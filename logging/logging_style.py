import logging

logging.basicConfig(
    # 方式一
    # format="%(asctime) - %(levelname) - %(message)", # 参数定义字符串
    # style="%", # style参数

    # 方式二
    format="$asctime - $levelname - $message", # 参数定义字符串
    style="$", # style参数

    # 方式三
    # format="{asctime} - {levelname} - {message}", # 参数定义字符串
    # style="{", # style参数
    
    datefmt="%Y-%m-%d %H:%M",
)

logging.error("Something went wrong!")

# 显示变量数据
name = "Samara"
logging.warning(f"{name=}") # 方式一，使用f-string进行插值
logging.debug("name=%s", name) # 方式二，使用模数运算符 ( %) 进行插值
# 输出格式为：2025-03-31 14:08 - WARNING - name='Samara'
