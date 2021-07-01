from setuptools import setup

setup(
    # Application name:
    name="broom",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Quentin Guilloteau",
    author_email="Quentin.Guilloteau@inria.fr",

    # Packages
    packages=["app"],

    # Include additional files into the package
    # include_package_data=True,
    entry_points={
        'console_scripts': ['broom=app.broom:main'],
    },

    # Details
    url="https://github.com/GuilloteauQ/broom",

    #
    # license="LICENSE.txt",
    description="simple local parameter sweep runner",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "pyyaml"
    ]
)
