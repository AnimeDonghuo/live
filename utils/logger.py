import logging
import sys
from logging.handlers import RotatingFileHandler
from bot.config import Config

def setup_logger():
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Bot Log
    bot_handler = RotatingFileHandler(
        Config.LOG_DIR / "bot.log", maxBytes=5*1024*1024, backupCount=5
    )
    bot_handler.setFormatter(log_format)
    
    # Error Log
    error_handler = RotatingFileHandler(
        Config.LOG_DIR / "error.log", maxBytes=5*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)

    # Console Output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(bot_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    # Specific logger for streams
    stream_logger = logging.getLogger("streamer")
    stream_handler = RotatingFileHandler(
        Config.LOG_DIR / "stream.log", maxBytes=10*1024*1024, backupCount=3
    )
    stream_handler.setFormatter(log_format)
    stream_logger.addHandler(stream_handler)
    
    return logger
