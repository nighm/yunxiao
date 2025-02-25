"""代码质量检查工具的安装配置

这个模块负责代码质量检查工具的打包和分发配置。
它使用setuptools来管理包的元数据、依赖关系和安装过程。
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code_quality_checker",
    version="0.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="代码质量检查工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code_quality_checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "code-quality-check=code_quality_checker.__main__:main",
        ],
    },
    install_requires=[
        "typing-extensions>=4.9.0",
        "astroid>=3.0.2",
        "pylint>=3.0.3"
    ],
    package_data={
        'code_quality_checker': ['README.md'],
    },
) 