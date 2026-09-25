from pathlib import Path
from datetime import datetime

# Retorna o dicionário com todas as categorias e suas extensões
def get_extensions_map() -> dict:
    return {
        "Imagens":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documentos":   [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx"],
        "Audios":       [".mp3", ".wav", ".aac", ".flac"],
        "Videos":       [".mp4", ".avi", ".mkv", ".mov"],
        "Arquivos":    [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executáveis": [".exe", ".msi", ".bat", ".sh"],
        "Códigos":        [".py", ".js", ".html", ".css", ".java", ".cpp"],
        "Outros":      []
    }

# Recebe uma extensão (ex: ".pdf") e retorna o nome da pasta destino (ex: "Documents")
def get_folder_for_extension(extension: str, extensions_map: dict) -> str:
    for folder, extensions in extensions_map.items():
        if extension in extensions:
            return folder
    return "Others"

# Verifica se o caminho informado existe e é um diretório válido
def verify_directory(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {"status": False, "message": f"O caminho '{path}' não existe."}
    if not p.is_dir():
        return {"status": False, "message": f"'{path}' não é um diretório válido."}
    return {"status": True, "message": f"Diretório '{path}' validado com sucesso."}

# Converte um número de bytes em string legível (KB, MB, GB...)
def _format_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

# Verifica se o arquivo existe e retorna seus metadados (tamanho, extensão, datas)
def verify_file(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {"exists": False, "is_file": False}
    if not p.is_file():
        return {"exists": True, "is_file": False}
    stat = p.stat()
    return {
        "exists": True,
        "is_file": True,
        "file_name": p.name,
        "extension": p.suffix.lower(),
        "size_bytes": stat.st_size,
        "size_readable": _format_size(stat.st_size),
        "creation_date": datetime.fromtimestamp(stat.st_ctime),
        "modification_date": datetime.fromtimestamp(stat.st_mtime),
    }

# Gera um caminho sem risco de sobrescrever arquivos existentes
def unique_path(target: Path) -> tuple[Path, bool]:
    if not target.exists():
        return target, False
    counter = 1
    while True:
        new_path = target.parent / f"{target.stem}_{counter}{target.suffix}"
        if not new_path.exists():
            return new_path, True
        counter += 1