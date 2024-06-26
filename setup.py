from setuptools import setup, find_namespace_packages

setup(
    name="Lana assistant bot",
    version="1.0.0",
    description="Team project Lana assistant bot",
    url="https://github.com/ViktorSvertoka/python-assistant-bot",
    author="python-assistant-bot",
    license="MIT",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["colorama", "prompt_toolkit", "tabulate"],
    entry_points={"console_scripts": ["hi-lana=main:main"]},
)
