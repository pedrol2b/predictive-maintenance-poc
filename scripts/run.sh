#!/bin/bash

# Script para executar a PoC de Manutenção Preditiva
# Uso: ./scripts/run.sh

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem Cor

echo -e "${BLUE}🚀 Iniciando PoC de Manutenção Preditiva...${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${YELLOW}⚠️  Execute este script a partir do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Ambiente virtual encontrado${NC}"
    PYTHON_CMD=".venv/bin/python"
else
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado, usando python do sistema${NC}"
    PYTHON_CMD="python"
fi

# Verificar se as dependências estão instaladas
echo -e "${BLUE}📦 Verificando dependências...${NC}"
$PYTHON_CMD -c "import pandas, numpy, sklearn" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Dependências não encontradas. Instale com: pip install -r requirements.txt${NC}"
    exit 1
}
echo -e "${GREEN}✓ Dependências verificadas${NC}"

echo ""
echo -e "${BLUE}▶️  Executando aplicação...${NC}"
echo ""

# Executar o script principal
$PYTHON_CMD src/main.py

echo ""
echo -e "${GREEN}✅ Execução concluída!${NC}"
