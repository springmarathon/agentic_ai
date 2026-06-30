from setuptools import setup, find_packages

setup(
    name="agentic_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=2.44.0",
        "python-dotenv>=1.2.2",
        "yfinance>=1.4.1",
    ],
)
