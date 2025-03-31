"""
存放日志，记录到文件
"""
import logging

logging.basicConfig(
    filename="app.log", # 文件名
    encoding="utf-8", # 编码格式
    filemode="a", # 模式，追加
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logging.warning("Save me!")
