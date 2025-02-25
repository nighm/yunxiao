import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def setup_logging():
    """配置日志系统"""
    # 创建日志目录
    log_file = os.getenv('LOG_FILE', 'output/automation.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # 设置日志级别
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return root_logger 