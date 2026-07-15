import time
from pathlib import Path
from tkinter import Tk, filedialog
from file_utils import verify_directory
from logger_config import setup_logger, log_event
from organizer import organize_by_type, organize_by_date, show_summary

# Função para selecionar o diretório usando Tkinter
def select_directory() -> str | None:
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Selecione a pasta para organizar")
    root.destroy()
    return directory if directory else None

# Função auxiliar para rodar a organização, contar o tempo e exibir o resumo
def run_action(action_func, directory: str, logger) -> None:
    start_time = time.time()
    stats = action_func(directory, logger)
    show_summary(stats, start_time, logger)

# Função principal 
def main() -> None:
    print("=========================================")
    print("      ORGANIZADOR DE ARQUIVOS V1.0       ")
    print("=========================================")

    directory = select_directory()
    if not directory:
        print("Seleção cancelada pelo usuário. Encerrando.")
        return
    validation = verify_directory(directory)
    if not validation["status"]:
        print(f"Erro: {validation['message']}")
        return
    logger = setup_logger(directory)
    log_event(logger, "info", f"Sessão iniciada no diretório: {directory}")
    actions = {
        "1": organize_by_type,
        "2": organize_by_date
    }
    while True:
        print(f"\n[Pasta Atual: {directory}]")
        print("Escolha o método de organização:")
        print("1. Organizar por tipo de arquivo (extensão)")
        print("2. Organizar por data de criação (Ano-Mês)")
        print("3. Alterar pasta de organização")
        print("4. Sair")
        choice = input("\nDigite o número da opção (1-4): ").strip()
        if choice in actions:
            run_action(actions[choice], directory, logger) 
        elif choice == "3":
            new_directory = select_directory()
            if not new_directory:
                print("Seleção cancelada. Mantendo a pasta atual.")
                continue   
            validation = verify_directory(new_directory)
            if not validation["status"]:
                print(f"Erro: {validation['message']}")
                continue
            directory = new_directory
            logger = setup_logger(directory)
            log_event(logger, "info", f"Pasta alterada para: {directory}")
        elif choice == "4":
            log_event(logger, "info", "Sessão encerrada pelo usuário.")
            print("Encerrando o organizador. Até logo!")
            break
        else: 
            print("Opção inválida. Por favor, escolha entre 1 e 4.")

if __name__ == "__main__":
    main()