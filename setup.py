from setuptools import setup, find_packages

setup(
    name="yunxiao-automation",
    version="0.2.0",
    description="云效自动化测试项目",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.18.1",
        "openpyxl>=3.1.2",
        "webdriver_manager>=4.0.1",
        "python-dotenv>=1.0.1",
        "typing-extensions>=4.9.0"
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-html>=4.1.1",
            "pytest-xdist>=3.5.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0"
        ]
    },
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "yunxiao-automation=src.core.automation.__main__:main",
            "code-quality-check=tools.code_quality_checker.code_quality_checker.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ]
) 