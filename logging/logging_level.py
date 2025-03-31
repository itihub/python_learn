"""
以下是五个默认日志级别，按严重程度递增的顺序排列：
DEBUG       logging.debug()     提供对作为开发人员的您有价值的详细信息。
INFO	    logging.info()	    提供有关程序运行情况的一般信息。
WARNING	    logging.warning()	表示您应该调查某些事情。
ERROR	    logging.error()	    提醒您程序中发生的意外问题。
CRITICAL    logging.critical()	告诉您发生了严重错误并且可能导致您的应用程序崩溃。

默认情况下，日志模块会记录严重性级别为或以上的消息WARNING。
"""
import logging

logging.basicConfig(
    level=logging.DEBUG,    # 调整日志级别
    format="%(levelname)s:%(name)s:%(message)s",    # 格式化输出
)

logging.debug("This is a debug message")

logging.info("This is an info message")

logging.warning("This is a warning message")

logging.error("This is an error message")

logging.critical("This is a critical message")

