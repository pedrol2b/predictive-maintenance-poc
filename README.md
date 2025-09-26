# predictive-maintenance-poc

<img width="696" height="484" alt="Image" src="https://github.com/user-attachments/assets/0edca82d-8869-4fcf-850b-0ef9b69ec143" />

## Prova de Conceito (PoC) de Manutenção Preditiva

Este projeto implementa uma Prova de Conceito simplificada para um sistema de Manutenção Preditiva utilizando Machine Learning. O sistema simula dados de sensores de máquinas industriais, treina um modelo de classificação para detectar falhas potenciais e demonstra a previsão de falhas em tempo real.

## Estrutura do Projeto

```bash
predictive-maintenance-poc/
├── pyproject.toml          # Configuração de testes e dependências
├── README.md               # Este arquivo
├── requirements.txt        # Dependências do projeto
├── scripts/                # Scripts de automação
│   ├── setup.sh           # Script de configuração inicial
│   ├── run.sh             # Script para executar a aplicação
│   ├── test.sh            # Script para executar testes com cobertura
│   ├── test-quick.sh      # Script para executar testes rápidos
│   ├── dev.sh             # Script de desenvolvimento (testes + execução)
│   └── docker-run.sh      # Script para executar com Docker
└── src/
    ├── __init__.py        # Torna src um pacote Python
    ├── main.py            # Script principal com lógica da PoC
    └── __tests__/
        ├── __init__.py    # Torna __tests__ um pacote Python
        └── main_test.py   # Testes abrangentes para todas as funções
```

## Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação principal
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica e arrays
- **Scikit-learn**: Biblioteca de Machine Learning (RandomForestClassifier)
- **Pytest**: Framework de testes unitários
- **Pytest-cov**: Cobertura de testes

## Como Executar

### Pré-requisitos

Certifique-se de ter Python 3.7+ instalado em seu sistema.

### Passos para Configuração

1. **Clone o repositório** (se aplicável):

    ```bash
    git clone https://github.com/pedrol2b/predictive-maintenance-poc.git
    ```

2. **Navegue até o diretório do projeto**:

    ```bash
    cd predictive-maintenance-poc
    ```

3. **Configure o ambiente (Recomendado)**:

    ```bash
    ./scripts/setup.sh
    ```

    Este script irá:
    - Criar um ambiente virtual Python
    - Instalar todas as dependências automaticamente
    - Verificar se tudo está configurado corretamente

    **Ou manualmente**:

    ```bash
    pip install -r requirements.txt
    ```

## Scripts de Automação

Para facilitar o uso do projeto, foram criados scripts de automação na pasta `scripts/`:

### 🛠️ Setup Inicial

```bash
./scripts/setup.sh
```

Configura automaticamente o ambiente Python com todas as dependências.

### 🚀 Executar a Aplicação

```bash
./scripts/run.sh
```

Executa a PoC de Manutenção Preditiva com verificações automáticas de ambiente e dependências.

### 🧪 Executar Testes Completos

```bash
./scripts/test.sh
```

Executa todos os testes com relatório de cobertura completo.

### ⚡ Executar Testes Rápidos

```bash
./scripts/test-quick.sh
```

Executa todos os testes sem cobertura para feedback mais rápido durante desenvolvimento.

### 🔧 Modo de Desenvolvimento

```bash
./scripts/dev.sh
```

Executa testes rápidos seguido da aplicação - ideal para desenvolvimento iterativo.

> 💡 **Vantagens dos Scripts**: Os scripts automatizam verificações de ambiente, fornecem feedback visual colorido e garantem que você está executando os comandos corretos.

## 🐳 Executar com Docker

Para usuários que preferem usar Docker ou não querem configurar o ambiente Python local, foi criado um setup completo com Docker.

### Pré-requisitos Docker

- [Docker](https://docker.com/get-started) instalado e rodando
- [Docker Compose](https://docs.docker.com/compose/install/) (geralmente incluído com Docker Desktop)

### Comandos Docker Simplificados

Use o script `docker-run.sh` para facilitar o uso:

```bash
# Construir e executar a aplicação
./scripts/docker-run.sh run

# Executar testes
./scripts/docker-run.sh test

# Abrir shell interativo no container
./scripts/docker-run.sh shell

# Executar em modo desenvolvimento (com volumes montados)
./scripts/docker-run.sh compose dev

# Limpar recursos Docker
./scripts/docker-run.sh cleanup
```

### Docker Manual

Alternativamente, você pode usar comandos Docker diretamente:

```bash
# Construir a imagem
docker build -t predictive-maintenance-poc .

# Executar a aplicação
docker run --rm predictive-maintenance-poc

# Executar testes
docker run --rm predictive-maintenance-poc python -m pytest src/__tests__ -v

# Shell interativo
docker run --rm -it predictive-maintenance-poc /bin/bash
```

### Docker Compose

Para desenvolvimento mais avançado:

```bash
# Executar aplicação
docker-compose run --rm predictive-maintenance

# Modo desenvolvimento (shell interativo)
docker-compose run --rm predictive-maintenance-dev

# Executar testes
docker-compose run --rm predictive-maintenance-test
```

## Execução Manual (Alternativa)

### Executando a PoC

Execute o script principal:

```bash
python src/main.py
```

### Executando os Testes

Para executar todos os testes:

```bash
pytest
```

Para executar testes com relatório de cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

Para executar testes em modo verbose:

```bash
pytest -v
```

**Nota**: Se você estiver usando um ambiente virtual (venv), certifique-se de que ele esteja ativado antes de executar os comandos acima.

## Testes e Cobertura

O projeto inclui uma suíte abrangente de testes automatizados que validam todas as funcionalidades principais:

### Estrutura de Testes

- **TestGenerateSensorData**: Testa a geração de dados sintéticos de sensores
  - Validação de parâmetros padrão e personalizados
  - Verificação de distribuição de falhas (~15%)
  - Teste de reprodutibilidade com semente aleatória
  - Validação de intervalos de valores dos sensores

- **TestPreprocessData**: Testa o pré-processamento de dados
  - Verificação de formato das saídas (X, y)
  - Validação das colunas de características
  - Consistência dos valores alvo

- **TestTrainModel**: Testa o treinamento do modelo
  - Verificação do tipo de modelo retornado
  - Capacidade de fazer predições
  - Validação de parâmetros do modelo

- **TestEvaluateModel**: Testa a avaliação do modelo
  - Retorno de métricas válidas
  - Formato do relatório de classificação
  - Casos de predições perfeitas

- **TestIntegration**: Testes de integração end-to-end
  - Pipeline completo de treinamento e predição
  - Limites de performance mínimos
  - Validação de predições em novos dados

- **TestEdgeCases**: Casos extremos e situações limite
  - Conjuntos de dados pequenos
  - Dados sem falhas (apenas operação normal)

### Cobertura de Código

Os testes cobrem todas as funções principais:

- `generate_sensor_data()`
- `preprocess_data()`
- `train_model()`
- `evaluate_model()`
- Fluxo de execução principal

Para visualizar relatório detalhado de cobertura:

```bash
pytest --cov=src --cov-report=html
# Abre htmlcov/index.html no navegador
```

## Saída Esperada

O script executará as seguintes ações e exibirá os resultados no console:

- Gerará dados simulados de sensores e mostrará o cabeçalho do DataFrame e distribuição de falhas
- Dividirá os dados em conjuntos de treinamento e teste
- Treinará um modelo `RandomForestClassifier`
- Avaliará o desempenho do modelo (precisão, recall, f1-score)
- Simulará novos pontos de dados (um normal, um potencialmente com falha) e predirá seu status
- Exibirá um alerta se uma falha potencial for detectada

## Exemplo de Saída

```text
Iniciando PoC de Manutenção Preditiva...

Cabeçalho dos Dados Simulados:
     sensor_1    sensor_2  sensor_3   sensor_4     sensor_5  fault
0  65.839212  127.901420  7.262432  17.771837   998.348737      1
1  49.308678   98.554813  4.968797  18.738138   974.817487      0
...

Distribuição de falhas:
 fault
0    1700
1     300
Name: count, dtype: int64

Formato dos dados de treinamento: (1400, 5)
Formato dos dados de teste: (600, 5)

Treinando modelo RandomForestClassifier...
Treinamento do modelo concluído.

Avaliando desempenho do modelo...
Precisão: 0.99
Relatório de Classificação:
               precision    recall  f1-score   support

           0       0.99      1.00      1.00       510
           1       1.00      0.97      0.98        90

    accuracy                           0.99       600
   macro avg       1.00      0.98      0.99       600
weighted avg       1.00      0.99      0.99       600

Simulando novos pontos de dados para predição em tempo real...
Predição para dados de operação normal: Normal
Predição para dados potencialmente defeituosos: Falha

ALERTA: Potencial falha detectada! Ação de manutenção recomendada.
PoC de Manutenção Preditiva finalizada.
```

## Funcionalidades Principais

### 1. Simulação de Dados de Sensores

- Geração de 5 tipos de sensores diferentes (temperatura, vibração, pressão, etc.)
- Simulação realista de condições normais vs. condições de falha
- Distribuição controlada de falhas (~15% do conjunto de dados)
- Dados reproduzíveis através de semente aleatória fixa

### 2. Pré-processamento de Dados

- Separação de características (X) e variável alvo (y)
- Dados prontos para algoritmos de Machine Learning
- Base para futuras melhorias em engenharia de características

### 3. Modelo de Machine Learning

- **Algoritmo**: Random Forest Classifier
- **Características**: 100 árvores, balanceamento de classes automático
- **Performance**: >99% de precisão nos dados de teste
- **Robustez**: Lida bem com classes desbalanceadas

### 4. Sistema de Predição em Tempo Real

- Capacidade de processar novos pontos de dados
- Classificação binária: Normal vs. Falha
- Sistema de alertas para manutenção preventiva

## Próximos Passos (para Implementação Completa)

Para um sistema pronto para produção, os próximos passos incluiriam:

### Melhorias Técnicas

- **Integração de Dados em Tempo Real**: Conectar com sistemas IoT e fluxos de dados de sensores reais
- **Engenharia de Características Avançada**:
  - Médias móveis, transformadas de Fourier (FFT)
  - Detecção de anomalias baseada em séries temporais
  - Análise de tendências e sazonalidade
- **Seleção e Otimização de Modelos**:
  - Comparação de múltiplos algoritmos (SVM, XGBoost, Neural Networks)
  - Hyperparameter tuning automatizado
  - Cross-validation robusta

### Infraestrutura e Deploy

- **Microsserviços**: API RESTful para predições em tempo real
- **Containerização**: Docker para deployment consistente
- **Monitoramento**: Logging, métricas de performance, alertas
- **Interface de Usuário**: Dashboard para visualização e monitoramento
- **Banco de Dados**: Armazenamento histórico de predições e feedback

### Manutenção e Evolução

- **Retreinamento Contínuo**: Pipeline automático com novos dados
- **A/B Testing**: Validação de novos modelos em produção
- **Feedback Loop**: Incorporação de resultados reais para melhoria do modelo
- **Escalabilidade**: Processamento distribuído para grandes volumes
