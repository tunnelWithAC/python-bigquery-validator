import setuptools

setuptools.setup(
    name="bigquery-validator",
    version="0.0.1",
    author="Conall Daly",
    author_email="conall.daly@livescore.com",
    description="Python module for validating BigQuery sql commands with support for Jinja templated variables",
    packages=setuptools.find_packages(),
    install_requires=[
        'google-cloud-bigquery',
        'Jinja2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    url=''
)
