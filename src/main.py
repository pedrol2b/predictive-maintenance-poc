
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Simulação de Dados (simplificada para PoC)
def generate_sensor_data(num_samples=1000):
    np.random.seed(42)
    # Simular 5 leituras de sensores (ex: temperatura, vibração, pressão, corrente, RPM)
    data = {
        'sensor_1': np.random.normal(loc=50, scale=5, size=num_samples),
        'sensor_2': np.random.normal(loc=100, scale=10, size=num_samples),
        'sensor_3': np.random.normal(loc=5, scale=1, size=num_samples),
        'sensor_4': np.random.normal(loc=20, scale=2, size=num_samples),
        'sensor_5': np.random.normal(loc=1000, scale=50, size=num_samples),
    }
    df = pd.DataFrame(data)

    # Introduzir 'falhas' baseadas em desvios nas leituras dos sensores
    # Tornar o sinal de falha mais distinto
    df['fault'] = 0
    num_faults = int(num_samples * 0.15) # 15% de falhas como objetivo
    fault_indices = np.random.choice(num_samples, num_faults, replace=False)

    # Para amostras com falha, aumentar significativamente as leituras dos sensores
    df.loc[fault_indices, 'sensor_1'] = np.random.normal(loc=65, scale=5, size=num_faults)
    df.loc[fault_indices, 'sensor_2'] = np.random.normal(loc=130, scale=10, size=num_faults)
    df.loc[fault_indices, 'sensor_3'] = np.random.normal(loc=8, scale=1, size=num_faults)
    df.loc[fault_indices, 'fault'] = 1

    return df

# 2. Pré-processamento (simplificado: sem valores ausentes, engenharia básica de features)
def preprocess_data(df):
    # Para esta PoC, usaremos dados brutos dos sensores como características
    # Em um cenário real, engenharia de características mais complexa (ex: médias móveis, FFT) seria aplicada
    X = df[['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']]
    y = df['fault']
    return X, y

# 3. Treinamento do Modelo
def train_model(X_train, y_train):
    # Usar class_weight para lidar com potencial desbalanceamento de classes
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    return model

# 4. Predição e Avaliação
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

# Fluxo principal de execução
if __name__ == "__main__":
    print("Iniciando PoC de Manutenção Preditiva...")

    # Gerar dados simulados
    sensor_data = generate_sensor_data(num_samples=2000)
    print("\nCabeçalho dos Dados Simulados:\n", sensor_data.head())
    print("\nDistribuição de falhas:\n", sensor_data['fault'].value_counts())

    # Pré-processar dados
    X, y = preprocess_data(sensor_data)

    # Dividir dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"\nFormato dos dados de treinamento: {X_train.shape}")
    print(f"Formato dos dados de teste: {X_test.shape}")

    # Treinar o modelo
    print("\nTreinando modelo RandomForestClassifier...")
    model = train_model(X_train, y_train)
    print("Treinamento do modelo concluído.")

    # Avaliar o modelo
    print("\nAvaliando desempenho do modelo...")
    accuracy, report = evaluate_model(model, X_test, y_test)
    print(f"Precisão: {accuracy:.2f}")
    print("Relatório de Classificação:\n", report)

    # Simular um novo ponto de dados para predição
    print("\nSimulando novos pontos de dados para predição em tempo real...")
    new_data_normal = pd.DataFrame([[50, 100, 5, 20, 1000]], columns=X.columns)
    new_data_faulty = pd.DataFrame([[68, 135, 8.5, 22, 1050]], columns=X.columns) # Valores indicando potencial falha

    prediction_normal = model.predict(new_data_normal)
    prediction_faulty = model.predict(new_data_faulty)

    print(f"Predição para dados de operação normal: {'Falha' if prediction_normal[0] == 1 else 'Normal'}")
    print(f"Predição para dados potencialmente defeituosos: {'Falha' if prediction_faulty[0] == 1 else 'Normal'}")

    if prediction_faulty[0] == 1:
        print("\nALERTA: Potencial falha detectada! Ação de manutenção recomendada.")
    else:
        print("\nNenhuma falha imediata detectada para o novo ponto de dados.")

    print("\nPoC de Manutenção Preditiva finalizada.")


