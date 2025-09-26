#!/bin/bash

# Script para executar todos os testes
# Uso: ./scripts/test.sh

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem Cor

echo -e "${BLUE}🧪 Executando testes da PoC de Manutenção Preditiva...${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "src/__tests__/main_test.py" ]; then
    echo -e "${RED}❌ Execute este script a partir do diretório raiz do projeto${NC}"
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

# Verificar se pytest está instalado
echo -e "${BLUE}📦 Verificando pytest...${NC}"
$PYTHON_CMD -c "import pytest" 2>/dev/null || {
    echo -e "${RED}❌ Pytest não encontrado. Instale com: pip install -r requirements.txt${NC}"
    exit 1
}
echo -e "${GREEN}✓ Pytest verificado${NC}"

echo ""
echo -e "${BLUE}▶️  Executando todos os testes...${NC}"
echo ""

# Executar testes com cobertura
$PYTHON_CMD -m pytest --cov=src --cov-report=term-missing -v

echo ""
echo -e "${GREEN}✅ Testes concluídos!${NC}"
