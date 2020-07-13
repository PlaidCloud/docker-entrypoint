from setuptools import setup, find_packages

setup(
    name='entrypoint',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        entrypoint=entrypoint.main:main
    ''',
)
