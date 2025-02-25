import time
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """重试装饰器
    
    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"重试{max_attempts}次后仍然失败: {str(e)}")
                        raise
                    logger.warning(f"第{attempts}次尝试失败，{delay}秒后重试: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def wait_for_condition(condition: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
    """等待条件满足
    
    Args:
        condition: 返回布尔值的条件函数
        timeout: 超时时间（秒）
        interval: 检查间隔（秒）
        
    Returns:
        bool: 条件是否满足
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(interval)
    return False

def safe_get_attribute(obj: Any, attr: str, default: Any = None) -> Any:
    """安全获取对象属性
    
    Args:
        obj: 目标对象
        attr: 属性名
        default: 默认值
        
    Returns:
        属性值或默认值
    """
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return default

def format_error(error: Exception) -> str:
    """格式化错误信息
    
    Args:
        error: 异常对象
        
    Returns:
        格式化后的错误信息
    """
    return f"{error.__class__.__name__}: {str(error)}" 