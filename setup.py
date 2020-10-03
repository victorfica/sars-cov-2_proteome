from setuptools import find_packages, setup

setup(
    name='sars2analysis',
    version='0.0.1',
    description='Code for SARS-CoV-2 Proteome Analysis',
    author='Victor Fica',
    license='MIT',
    packages=find_packages(),
    entry_points={
        "console_scripts": ['sarscov2_processing = src.process_raw:main']}
)
