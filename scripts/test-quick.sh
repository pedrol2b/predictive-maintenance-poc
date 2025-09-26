#!/bin/bash

# Script para executar testes rápidos (sem cobertura)
# Uso: ./scripts/test-quick.sh

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem Cor

echo -e "${BLUE}⚡ Executando testes rápidos...${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "src/__tests__/main_test.py" ]; then
    echo -e "${RED}❌ Execute este script a partir do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ -d ".venv" ]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

# Executar testes sem cobertura para execução mais rápida
$PYTHON_CMD -m pytest -v

echo ""
echo -e "${GREEN}✅ Testes rápidos concluídos!${NC}"
