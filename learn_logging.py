import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

logger.debug("这条不会显示（级别低于 INFO）")
logger.info("程序启动，准备查询汇率")
logger.warning("接口响应较慢（1.8 秒）")
logger.error("接口返回 500")