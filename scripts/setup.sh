#!/bin/bash

# Script de configuração inicial do projeto
# Uso: ./scripts/setup.sh

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem Cor

echo -e "${BLUE}🛠️  Configurando ambiente da PoC de Manutenção Preditiva...${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Execute este script a partir do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado. Instale Python 3.7+ primeiro.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 encontrado${NC}"

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}📦 Criando ambiente virtual...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${GREEN}✓ Ambiente virtual já existe${NC}"
fi

# Ativar ambiente virtual e instalar dependências
echo -e "${BLUE}📦 Instalando dependências...${NC}"
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo ""
echo -e "${GREEN}✅ Configuração concluída!${NC}"
echo ""
echo -e "${YELLOW}💡 Próximos passos:${NC}"
echo -e "   • Execute: ${BLUE}./scripts/run.sh${NC} para rodar a aplicação"
echo -e "   • Execute: ${BLUE}./scripts/test.sh${NC} para rodar os testes"
echo -e "   • Execute: ${BLUE}./scripts/test-quick.sh${NC} para testes rápidos"
echo ""
