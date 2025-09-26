#!/bin/bash

# Script de desenvolvimento - executa testes e depois a aplicação
# Uso: ./scripts/dev.sh

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # Sem Cor

echo -e "${PURPLE}🔧 Modo de Desenvolvimento - PoC Manutenção Preditiva${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "src/main.py" ]; then
    echo -e "${YELLOW}⚠️  Execute este script a partir do diretório raiz do projeto${NC}"
    exit 1
fi

# Executar testes rápidos primeiro
echo -e "${BLUE}1️⃣  Executando testes rápidos...${NC}"
./scripts/test-quick.sh

echo ""
echo -e "${BLUE}2️⃣  Executando aplicação...${NC}"
./scripts/run.sh

echo ""
echo -e "${GREEN}🎉 Desenvolvimento concluído - Testes ✓ e Aplicação ✓${NC}"
