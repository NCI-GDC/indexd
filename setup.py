from setuptools import setup, find_packages

setup(
    name='indexd',
    version='0.1',
    packages=find_packages(),
    package_data={
        'index': [
            'schemas/*',
        ]
    },
    install_requires=[
        'flask==0.12.4',
        'jsonschema==2.5.1',
        'psycopg2-binary==2.8.2',
        'sqlalchemy==1.3.3',
        'sqlalchemy-utils>=0.32.21',
        'future>=0.16.0,<1.0.0',
        'requests==2.22.0',
    ],
)
