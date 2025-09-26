import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Importar do módulo src
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import (
    generate_sensor_data,
    preprocess_data,
    train_model,
    evaluate_model
)


class TestGenerateSensorData:
    """Testar a função generate_sensor_data."""

    def test_generate_sensor_data_default_params(self):
        """Testar geração de dados com parâmetros padrão."""
        df = generate_sensor_data()

        # Verificar forma e colunas
        assert df.shape[0] == 1000  # num_samples padrão
        expected_columns = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'fault']
        assert list(df.columns) == expected_columns

        # Verificar tipos de dados
        for col in expected_columns:
            assert pd.api.types.is_numeric_dtype(df[col])

        # Verificar se a coluna fault contém apenas 0s e 1s
        assert set(df['fault'].unique()).issubset({0, 1})

    def test_generate_sensor_data_custom_samples(self):
        """Testar geração de dados com número personalizado de amostras."""
        num_samples = 500
        df = generate_sensor_data(num_samples=num_samples)

        assert df.shape[0] == num_samples

    def test_generate_sensor_data_fault_percentage(self):
        """Testar que aproximadamente 15% das amostras são falhas."""
        df = generate_sensor_data(num_samples=2000)
        fault_percentage = df['fault'].sum() / len(df)

        # Permitir alguma tolerância (±3%) devido à amostragem aleatória
        assert 0.12 <= fault_percentage <= 0.18

    def test_generate_sensor_data_reproducibility(self):
        """Testar que a função produz resultados reproduzíveis."""
        df1 = generate_sensor_data(num_samples=100)
        df2 = generate_sensor_data(num_samples=100)

        # Devem ser idênticos devido à semente aleatória fixa
        pd.testing.assert_frame_equal(df1, df2)

    def test_generate_sensor_data_sensor_ranges(self):
        """Testar que os valores dos sensores estão dentro dos intervalos esperados."""
        df = generate_sensor_data(num_samples=1000)

        # Para dados normais (fault=0), verificar se os intervalos dos sensores são razoáveis
        normal_data = df[df['fault'] == 0]

        # Estes intervalos consideram distribuição normal com alguma tolerância (±4 desvios padrão)
        assert normal_data['sensor_1'].between(30, 70).all()
        assert normal_data['sensor_2'].between(60, 140).all()
        assert normal_data['sensor_3'].between(1, 9).all()
        assert normal_data['sensor_4'].between(12, 28).all()
        assert normal_data['sensor_5'].between(800, 1200).all()


class TestPreprocessData:
    """Testar a função preprocess_data."""

    def test_preprocess_data_shape(self):
        """Testar que o pré-processamento retorna formas corretas."""
        df = generate_sensor_data(num_samples=100)
        X, y = preprocess_data(df)

        assert X.shape == (100, 5)  # 5 colunas de sensores
        assert y.shape == (100,)    # coluna alvo

    def test_preprocess_data_columns(self):
        """Testar que X contém as colunas corretas dos sensores."""
        df = generate_sensor_data(num_samples=100)
        X, y = preprocess_data(df)

        expected_features = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']
        assert list(X.columns) == expected_features

    def test_preprocess_data_target_values(self):
        """Testar que y contém os valores alvo corretos."""
        df = generate_sensor_data(num_samples=100)
        X, y = preprocess_data(df)

        # Alvo deve conter apenas 0s e 1s
        assert set(y.unique()).issubset({0, 1})

        # Deve corresponder à coluna fault original
        pd.testing.assert_series_equal(y, df['fault'], check_names=False)


class TestTrainModel:
    """Testar a função train_model."""

    def test_train_model_returns_classifier(self):
        """Testar que o treinamento retorna um RandomForestClassifier."""
        df = generate_sensor_data(num_samples=200)
        X, y = preprocess_data(df)

        model = train_model(X, y)

        assert isinstance(model, RandomForestClassifier)

    def test_train_model_can_predict(self):
        """Testar que o modelo treinado pode fazer predições."""
        df = generate_sensor_data(num_samples=200)
        X, y = preprocess_data(df)

        model = train_model(X, y)
        predictions = model.predict(X)

        assert len(predictions) == len(X)
        assert set(predictions).issubset({0, 1})

    def test_train_model_parameters(self):
        """Testar que o modelo tem parâmetros corretos."""
        df = generate_sensor_data(num_samples=200)
        X, y = preprocess_data(df)

        model = train_model(X, y)

        assert model.n_estimators == 100
        assert model.random_state == 42
        assert model.class_weight == 'balanced'


class TestEvaluateModel:
    """Testar a função evaluate_model."""

    def test_evaluate_model_returns_metrics(self):
        """Testar que a avaliação retorna acurácia e relatório."""
        df = generate_sensor_data(num_samples=200)
        X, y = preprocess_data(df)

        # Divisão simples treino-teste para teste
        split_idx = int(0.7 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        model = train_model(X_train, y_train)
        accuracy, report = evaluate_model(model, X_test, y_test)

        # Verificar tipos de retorno e intervalos
        assert isinstance(accuracy, (float, np.floating))
        assert 0 <= accuracy <= 1
        assert isinstance(report, str)
        assert 'precision' in report
        assert 'recall' in report
        assert 'f1-score' in report

    def test_evaluate_model_perfect_prediction(self):
        """Testar avaliação com predições perfeitas."""
        # Criar dados de teste simples
        X_test = pd.DataFrame({
            'sensor_1': [50, 65],
            'sensor_2': [100, 130],
            'sensor_3': [5, 8],
            'sensor_4': [20, 22],
            'sensor_5': [1000, 1050]
        })
        y_test = pd.Series([0, 1])

        # Criar um modelo mock que prediz perfeitamente
        class MockModel:
            def predict(self, X):
                # Regra simples: se sensor_1 > 60, prever falha
                return (X['sensor_1'] > 60).astype(int)

        model = MockModel()
        accuracy, report = evaluate_model(model, X_test, y_test)

        assert accuracy == 1.0  # Acurácia perfeita


class TestIntegration:
    """Testes de integração para o pipeline completo."""

    def test_complete_pipeline(self):
        """Testar o pipeline completo de manutenção preditiva."""
        # Gerar dados
        sensor_data = generate_sensor_data(num_samples=300)

        # Pré-processar
        X, y = preprocess_data(sensor_data)

        # Divisão treino-teste
        split_idx = int(0.7 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Treinar modelo
        model = train_model(X_train, y_train)

        # Avaliar
        accuracy, report = evaluate_model(model, X_test, y_test)

        # Verificar que obtemos resultados razoáveis
        assert accuracy > 0.5  # Deve ser melhor que aleatório
        assert 'precision' in report

        # Testar predição em novos dados
        new_normal = pd.DataFrame([[50, 100, 5, 20, 1000]], columns=X.columns)
        new_faulty = pd.DataFrame([[68, 135, 8.5, 22, 1050]], columns=X.columns)

        pred_normal = model.predict(new_normal)
        pred_faulty = model.predict(new_faulty)

        # Predições devem ser binárias
        assert pred_normal[0] in [0, 1]
        assert pred_faulty[0] in [0, 1]

    def test_model_performance_threshold(self):
        """Testar que o modelo atinge o limiar mínimo de performance."""
        # Usar conjunto de dados maior para medição de performance mais confiável
        sensor_data = generate_sensor_data(num_samples=1000)
        X, y = preprocess_data(sensor_data)

        # Divisão 70-30
        split_idx = int(0.7 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        model = train_model(X_train, y_train)
        accuracy, _ = evaluate_model(model, X_test, y_test)

        # O modelo deve atingir pelo menos 75% de acurácia nestes dados sintéticos
        assert accuracy >= 0.75, f"Acurácia do modelo {accuracy:.3f} abaixo do limiar"


class TestEdgeCases:
    """Testar casos extremos e condições de erro."""

    def test_empty_data_handling(self):
        """Testar comportamento com dados mínimos."""
        # Conjunto de dados muito pequeno
        df = generate_sensor_data(num_samples=10)
        X, y = preprocess_data(df)

        # Ainda deve funcionar com dados pequenos
        assert len(X) == 10
        assert len(y) == 10

    def test_all_normal_data(self):
        """Testar com conjunto de dados não contendo falhas."""
        # Criar dados sem falhas
        np.random.seed(42)
        data = {
            'sensor_1': np.random.normal(50, 5, 100),
            'sensor_2': np.random.normal(100, 10, 100),
            'sensor_3': np.random.normal(5, 1, 100),
            'sensor_4': np.random.normal(20, 2, 100),
            'sensor_5': np.random.normal(1000, 50, 100),
            'fault': np.zeros(100)  # Todos normais
        }
        df = pd.DataFrame(data)

        X, y = preprocess_data(df)

        # Todos os alvos devem ser 0
        assert (y == 0).all()

        # Treinamento do modelo ainda deve funcionar (embora possa não ser muito útil)
        model = train_model(X, y)
        predictions = model.predict(X)

        # Todas as predições provavelmente serão 0 devido ao desequilíbrio de classes
        assert all(pred in [0, 1] for pred in predictions)


if __name__ == "__main__":
    # Executar testes se o script for executado diretamente
    pytest.main([__file__, "-v"])
