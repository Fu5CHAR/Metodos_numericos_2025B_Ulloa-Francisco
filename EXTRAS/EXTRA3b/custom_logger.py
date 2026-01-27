import logging
import requests
import colorlog


class TelegramHandler(logging.Handler):
    """Handler personalizado para enviar logs a Telegram"""

    def __init__(self, token: str, chat_id: str, timeout: int = 3):
        super().__init__()
        self.token = token
        self.chat_id = chat_id
        self.timeout = timeout

    def emit(self, record):
        log_entry = self.format(record)
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": log_entry
        }
        try:
            requests.post(url, data=payload, timeout=self.timeout)
        except Exception:
            # Nunca romper la ejecución por un fallo de Telegram
            pass


class CustomLogger:
    """
    Logger reutilizable:
    - Consola (con colores)
    - Archivo .log
    - Telegram (opcional)
    """

    def __init__(
        self,
        name: str = "app_logger",
        log_file: str = "app.log",
        level=logging.DEBUG,
        telegram_token: str | None = None,
        telegram_chat_id: str | None = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Evita duplicar logs si se importa varias veces (muy importante en Jupyter)
        if self.logger.handlers:
            return

        log_format = (
            "%(asctime)s | %(levelname)-8s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )
        date_format = "%Y-%m-%d %H:%M:%S"

        self._add_console_handler(log_format, date_format)
        self._add_file_handler(log_file, log_format, date_format)

        if telegram_token and telegram_chat_id:
            self._add_telegram_handler(
                telegram_token,
                telegram_chat_id,
                log_format,
                date_format
            )

    def _add_console_handler(self, log_format, date_format):
        console_handler = logging.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s" + log_format,
            datefmt=date_format,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self, log_file, log_format, date_format):
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            log_format,
            datefmt=date_format
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def _add_telegram_handler(
        self,
        token,
        chat_id,
        log_format,
        date_format
    ):
        telegram_handler = TelegramHandler(token, chat_id)
        telegram_formatter = logging.Formatter(
            "🚨 LOG 🚨\n" + log_format,
            datefmt=date_format
        )
        telegram_handler.setFormatter(telegram_formatter)
        telegram_handler.setLevel(logging.ERROR)
        self.logger.addHandler(telegram_handler)

    def get_logger(self):
        return self.logger




