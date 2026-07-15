# File Organizer CLI
Um organizador de arquivos automático escrito em Python para organizar diretórios bagunçados por extensão ou por data de criação. Desenvolvido com foco em boas práticas de programação, modularidade e registro detalhado de logs.

## Funcionalidades
- **Organização por Extensão:** Identifica tipos comuns de arquivos (Imagens, Documentos, Áudio, etc.) e os move para pastas categorizadas.
- **Organização por Data:** Cria pastas baseadas no ano e mês de criação (`YYYY-MM`) dos arquivos.
- **Prevenção de Colisões:** Se um arquivo com o mesmo nome já existir na pasta de destino, ele é renomeado automaticamente com um sufixo numérico (ex: `foto_1.png`) para evitar sobrescritas.
- **Logs de Auditoria:** Registra todas as ações executadas em arquivos `.log` dinâmicos dentro de uma subpasta `_logs`.
- **Interface Gráfica para Seleção:** Utiliza Tkinter para permitir que o usuário selecione a pasta de forma visual e amigável.

## Tecnologias Utilizadas
- **Python 3.x**
- **Pathlib** (Manipulação moderna de caminhos no sistema)
- **Tkinter** (Diálogos de interface gráfica)
- **Logging** (Rastreabilidade de eventos do sistema)
- **Shutil** (Operações de arquivos de alto nível)

## Estrutura do Projeto
- `main.py`: Ponto de entrada do sistema contendo o menu interativo e interface de usuário.
- `organizer.py`: Lógica central para movimentação e execução das regras de negócio de organização.
- `file_utils.py`: Funções utilitárias para verificação de metadados dos arquivos e criação de caminhos únicos.
- `logger_config.py`: Módulo responsável pela parametrização dos logs.

## Como Executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
2. Acesse a pasta do projeto:
    cd nome-do-repositorio
3. Execute o script principal:
    python main.py