#!/bin/bash

# Script Docker para PoC de Manutenção Preditiva
# Uso: ./scripts/docker-run.sh [comando]

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sem Cor

# Verificar se Docker está instalado e rodando
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker não está instalado. Por favor, instale o Docker primeiro.${NC}"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker não está rodando. Por favor, inicie o Docker primeiro.${NC}"
        exit 1
    fi
}

# Construir a imagem Docker
build_image() {
    echo -e "${BLUE}🏗️  Construindo imagem Docker...${NC}"
    docker build -t predictive-maintenance-poc .
    echo -e "${GREEN}✅ Imagem Docker construída com sucesso!${NC}"
}

# Executar a aplicação principal
run_app() {
    echo -e "${BLUE}🚀 Executando PoC de Manutenção Preditiva no Docker...${NC}"
    docker run --rm predictive-maintenance-poc
}

# Executar testes
run_tests() {
    echo -e "${BLUE}🧪 Executando testes no Docker...${NC}"
    docker run --rm \
        -v "$(pwd):/app" \
        predictive-maintenance-poc \
        python -m pytest src/__tests__ -v --cov=src --cov-report=term-missing
}

# Executar shell interativo
run_shell() {
    echo -e "${BLUE}🐚 Abrindo shell interativo no container Docker...${NC}"
    docker run --rm -it \
        -v "$(pwd):/app" \
        predictive-maintenance-poc \
        /bin/bash
}

# Executar com docker-compose
run_compose() {
    echo -e "${BLUE}🐳 Executando com Docker Compose...${NC}"
    case $1 in
        "dev")
            docker-compose run --rm predictive-maintenance-dev
            ;;
        "test")
            docker-compose run --rm predictive-maintenance-test
            ;;
        *)
            docker-compose run --rm predictive-maintenance
            ;;
    esac
}

# Limpar recursos Docker
cleanup() {
    echo -e "${YELLOW}🧹 Limpando recursos Docker...${NC}"
    docker-compose down 2>/dev/null || true
    if docker images | grep -q predictive-maintenance-poc; then
        docker rmi predictive-maintenance-poc 2>/dev/null || true
    fi
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
}

# Mostrar uso
show_usage() {
    echo -e "${BLUE}🚀 PoC Manutenção Preditiva - Executor Docker${NC}"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos:"
    echo "  build       Construir a imagem Docker"
    echo "  run         Executar a aplicação principal"
    echo "  test        Executar testes"
    echo "  shell       Abrir shell interativo"
    echo "  compose     Executar com docker-compose (opções: dev, test)"
    echo "  cleanup     Remover imagens e containers Docker"
    echo "  help        Mostrar esta mensagem de ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 build"
    echo "  $0 run"
    echo "  $0 test"
    echo "  $0 shell"
    echo "  $0 compose dev"
    echo "  $0 cleanup"
}

# Lógica principal do script
main() {
    # Verificar se estamos no diretório correto
    if [ ! -f "src/main.py" ]; then
        echo -e "${RED}⚠️  Execute este script a partir do diretório raiz do projeto${NC}"
        exit 1
    fi

    # Verificar disponibilidade do Docker
    check_docker

    # Tratar argumentos da linha de comando
    case ${1:-run} in
        "build")
            build_image
            ;;
        "run")
            build_image
            run_app
            ;;
        "test")
            build_image
            run_tests
            ;;
        "shell")
            build_image
            run_shell
            ;;
        "compose")
            run_compose $2
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            echo -e "${RED}❌ Comando desconhecido: $1${NC}"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Executar função principal com todos os argumentos
main "$@"
