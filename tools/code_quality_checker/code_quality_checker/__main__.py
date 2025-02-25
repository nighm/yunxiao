"""代码质量检查工具的命令行入口"""

import argparse
import logging
import sys
from pathlib import Path
from .checker import CodeQualityChecker

def setup_logging(verbose: bool = False):
    """配置日志系统
    
    Args:
        verbose: 是否输出详细日志
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="代码质量检查工具")
    parser.add_argument("path", help="要检查的项目路径")
    parser.add_argument("--changed-only", action="store_true", help="只检查变更的文件")
    parser.add_argument("--days", type=int, default=7, help="检查最近几天的变更（默认7天）")
    parser.add_argument("--report", help="输出报告的文件路径")
    parser.add_argument("--exclude", nargs="+", help="要排除的文件/目录模式")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出详细日志")
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    try:
        checker = CodeQualityChecker(args.path, args.exclude)
        report = checker.generate_report(args.changed_only, args.days)
        
        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {args.report}")
        else:
            print(report)
            
    except Exception as e:
        logging.error(f"执行过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 