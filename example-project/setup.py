from setuptools import setup, find_packages

setup(
    name="example-project",
    version="1.0.0",
    description="Baibai 发布示例项目",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "example=example_project.cli:main",
        ],
    },
)
