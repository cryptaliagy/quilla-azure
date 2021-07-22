from setuptools import setup, find_packages


setup(
    name='quilla-azure',
    author='Natalia Maximo',
    author_email='iam@natalia.dev',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['quilla'],
    tests_require=['flake8', 'mypy'],
    extras_require={
        'tests': ['flake8', 'mypy'],
    },
    entry_points={
        'QuillaPlugins': [
            'azure = quilla_azure:QuillaAzure'
        ]
    },
)
