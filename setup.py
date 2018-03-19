"""Setup file for the Alexa Skill python module."""
from setuptools import setup, find_packages

setup(
    name='alexa',
    version='0.0.1',
    description='Alexa Skill Library',
    author='Neil Stewart',
    author_email='neil@njsn.uk',
    keywords='alexa skills dev voice library',
    test_suite='tests',
    # package_data={'PythonAlexa': ['tag_config.yaml']},
    packages=find_packages(exclude=['docs', 'tests', 'contrib']),
    install_requires=['boto3']
)
