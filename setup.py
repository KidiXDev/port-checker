from setuptools import setup, find_packages

setup(
    name="pychkr",
    description="PyChkr - A Python utility to check port availability on the local system.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license='MIT',
    author='KidiXDev',
    author_email='kidixdev@logiclab.id',
    url='https://github.com/KidiXDev/port-checker',
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "pychkr=pychkr.main:main",
        ],
    }
)
