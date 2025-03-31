import logging

print(__name__)
# 实例化记录器
logger = logging.getLogger(__name__)
logger.warning("Look at my logger!")
