import shutil
import logging
import time
from pathlib import Path
from datetime import datetime
from file_utils import (
    get_extensions_map,
    get_folder_for_extension,
    verify_file,
    unique_path,
)
from logger_config import log_event

# Move um arquivo para a pasta destino com segurança (sem sobrescrever)
def move_file(
    file_path: Path,
    folder_name: str,
    base_dir: Path,
    logger: logging.Logger,
    stats: dict
) -> None:
    try:
        dest_folder = base_dir / folder_name
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_path, was_renamed = unique_path(dest_folder / file_path.name)
        shutil.move(str(file_path), str(dest_path))
        if was_renamed:
            stats["renamed"] += 1
            log_event(logger, "warning", f"Movido e renomeado: {file_path.name} → {folder_name}/{dest_path.name}")
        else:
            stats["moved"] += 1
            log_event(logger, "info", f"Movido: {file_path.name} → {folder_name}/")
    except Exception as e:
        stats["errors"] += 1
        log_event(logger, "error", f"Erro ao mover {file_path.name}: {str(e)}")

# Organiza todos os arquivos do diretório em subpastas por categoria (Images, Documents...)
def organize_by_type(directory: str, logger: logging.Logger) -> dict:
    stats = {"moved": 0, "renamed": 0, "errors": 0}
    extensions_map = get_extensions_map()
    base_dir = Path(directory)
    log_event(logger, "info", "Organização por tipo iniciada")
    for file_path in base_dir.iterdir():
        if file_path.is_dir():
            continue
        file_info = verify_file(str(file_path))
        if not file_info.get("exists") or not file_info.get("is_file"):
            continue
        extension = file_info["extension"]
        folder_name = get_folder_for_extension(extension, extensions_map)
        move_file(file_path, folder_name, base_dir, logger, stats)  
    log_event(logger, "info", "Organização por tipo concluída")
    return stats

# Organiza todos os arquivos do diretório em subpastas por data (ex: 2026-07/)
def organize_by_date(directory: str, logger: logging.Logger) -> dict:
    stats = {"moved": 0, "renamed": 0, "errors": 0}
    base_dir = Path(directory)
    log_event(logger, "info", "Organização por data iniciada")   
    for file_path in base_dir.iterdir():
        # Pulamos pastas
        if file_path.is_dir():
            continue
        file_info = verify_file(str(file_path))
        if not file_info.get("exists") or not file_info.get("is_file"):
            continue
        date_created = file_info["creation_date"]
        try:
            folder_name = date_created.strftime("%Y-%m")
        except Exception as e:
            log_event(logger, "error", f"Falha ao ler data de {file_path.name}: {e}")
            stats["errors"] += 1
            continue
        move_file(file_path, folder_name, base_dir, logger, stats)
    log_event(logger, "info", "Organização por data concluída")
    return stats

# Exibe no terminal e no log um resumo da operação realizada
def show_summary(stats: dict, start_time: float, logger: logging.Logger) -> None:
    elapsed_time = time.time() - start_time
    lines = [
        "=========================================",
        "        RESUMO DA ORGANIZAÇÃO",
        "=========================================",
        f"  Arquivos movidos:     {stats.get('moved', 0)}",
        f"  Arquivos renomeados:   {stats.get('renamed', 0)}",
        f"  Erros encontrados:    {stats.get('errors', 0)}",
        f"  Tempo decorrido:      {elapsed_time:.2f} segundos",
        "========================================="
    ]
    summary = "\n".join(lines)
    log_event(logger, "info", f"\n{summary}")
    print(summary)
    