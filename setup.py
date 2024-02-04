from setuptools import setup, find_packages

setup(
    name='apitest',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
        'allure-pytest'
        # 添加其他依赖
    ],
)
