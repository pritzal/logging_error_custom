from setuptools import setup, find_packages

setup(
    name='logging_error_custom',
    version='0.13',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'python-dotenv'
    ],
    description='A library for logging exceptions to a MySQL database.',
    author='Aayush Chaudhary',
    author_email='aayush18702@example.com',
)
