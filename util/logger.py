from loguru import logger
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent



class CustomLogger:
    _log_path: Path

    def __init__(self, name: str) -> None:
        self._logger = logger.bind(name=name)
        self._log_path = BASE_DIR / "logs" / f"{name}.log"

        self._logger.add(self._log_path, rotation="10 MB")
    
    def info(self, message: str, _print: bool = False) -> None:
        self._logger.info(message)
        if _print:
            print(message)

    def error(self, message: str, _print: bool = False) -> None:
        self._logger.error(message)
        if _print:
            print(message)

    
    def warning(self, message: str, _print: bool = False) -> None:
        self._logger.warning(message)
        if _print:
            print(message)
    
    def debug(self, message: str, _print: bool = False) -> None:
        self._logger.debug(message)
        if _print:
            print(message)
    
    def critical(self, message: str, _print: bool = False) -> None:
        self._logger.critical(message)
        if _print:
            print(message)
    
    def exception(self, message: str, _print: bool = False) -> None:
        self._logger.exception(message)
        if _print:
            print(message)
    
    def success(self, message: str, _print: bool = False) -> None:
        self._logger.success(message)
        if _print:
            print(message)
    
    def log(self, message: str, _print: bool = False) -> None:
        self._logger.log(message)
        if _print:
            print(message)
    
    def trace(self, message: str, _print: bool = False) -> None:
        self._logger.trace(message)
        if _print:
            print(message)
        

