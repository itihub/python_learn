"""
使用logging模块捕获应用程序中的完整堆栈跟踪
"""
import logging

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

donuts = 5
guests = 0
try:
    donuts_per_guest = donuts / guests
except ZeroDivisionError:
    logging.error("DonutCalculationError", exc_info=True) # exc_info设置为True，打印有关异常的任何信息
    logging.exception("DonutCalculationError") # 等价于上面的打印，调用logging.exception()类似于调用logging.error(exc_info=True)
