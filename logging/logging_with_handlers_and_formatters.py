import logging

# 实例化记录器
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
formatter = logging.Formatter("{levelname} - {message}", style="{")

# 用于将日志输出到控制台标准输出流
console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
# 添加到记录器
logger.addHandler(console_handler)

# 用于将日志记录写入文件
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter)
# 添加到记录器
logger.addHandler(file_handler)


logger.debug("Just checking in!")

logger.warning("Stay curious!")

logger.error("Stay put!")
