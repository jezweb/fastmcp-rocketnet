"""
Setup script for rocketnet-shared package
"""

from setuptools import setup, find_packages

setup(
    name="rocketnet-shared",
    version="1.0.0",
    description="Shared utilities for Rocket.net MCP servers",
    author="Jezweb",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
)