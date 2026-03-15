# Modules
import logging
# ===================================================================== #

class StreamFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
    }
    DATE_COLOR = "\033[96m"
    RESET = "\033[0m"
    WHITE = "\033[97m"

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, self.RESET)
        fmt = (
            f"{self.DATE_COLOR}%(asctime)s{self.RESET} "
            f"[{level_color}%(levelname)s{self.RESET}] "
            f"{self.WHITE}%(message)s{self.RESET}"
        )
        formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")
        return formatter.format(record)
# --------------------------------------------------------------------- #

def setup_logger(file: str, debug=True) -> logging.Logger:
    logger = logging.getLogger(file)
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(file, mode="w")
    file_handler.setFormatter(logging.Formatter(
        f'"%(asctime)s", "%(levelname)s", "%(message)s"',
        datefmt=r"%d-%m-%Y %H:%M:%S"
    ))
    logger.addHandler(file_handler)

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(StreamFormatter())
    
    if (debug):
        logger.addHandler(stream_handler)

    return logger
# --------------------------------------------------------------------- #