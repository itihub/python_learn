import logging


# 过滤日志
def show_only_debug(record):
    return record.levelname == "DEBUG"


# 实例化记录器
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter("{levelname} - {message}", style="{")

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
console_handler.addFilter(show_only_debug)
logger.addHandler(console_handler)

# 将日志记录在文件
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.debug("Just checking in!")
logger.warning("Stay curious!")
logger.error("Stay put!")
