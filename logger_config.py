import logging
from pathlib import Path
from datetime import datetime

# Cria e configura o logger com saída no terminal e em arquivo .log
def setup_logger(directory: str) -> logging.Logger:
    log_dir = Path(directory) / "_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_path = log_dir / f"organizador_{timestamp}.log"
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if logger.handlers:
        logger.handlers.clear()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

# Registra uma mensagem no log no nível adequado
def log_event(logger: logging.Logger, level: str, message: str) -> None:
    dispatch = {
        "debug":    logger.debug,
        "info":     logger.info,
        "warning":  logger.warning,
        "warn":     logger.warning,
        "error":    logger.error,
        "critical": logger.critical,
    }
    log_func = dispatch.get(level.strip().lower(), logger.info)
    log_func(message)
    