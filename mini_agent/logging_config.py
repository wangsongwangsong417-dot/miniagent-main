"""
项目日志配置模块
"""
import logging
import sys
from typing import Optional


def configure_logging(
    log_level: int = logging.INFO,
    log_format: str = "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    配置项目日志

    Args:
        log_level: 日志级别
        log_format: 日志格式
        log_file: 日志文件路径（None 表示输出到控制台）

    Returns:
        配置好的 logger 实例
    """
    # 创建 logger
    logger = logging.getLogger("miniagent")
    logger.setLevel(log_level)
    logger.handlers.clear()

    # 创建格式化器
    formatter = logging.Formatter(log_format)

    # 控制台输出 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出 handler（如果指定了文件）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 创建项目全局 logger
logger = configure_logging()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取 logger 实例

    Args:
        name: logger 名称（None 表示使用全局 logger）

    Returns:
        logger 实例
    """
    if name:
        return logging.getLogger(f"miniagent.{name}")
    return logger
