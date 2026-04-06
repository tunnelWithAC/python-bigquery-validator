import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-bigquery-validator",
    version="1.0.1",
    author="Conall Daly",
    author_email="conalldalydev@gmail.com",
    description="Python module for validating BigQuery sql queries with support for Jinja templated variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tunnelWithAC/python-bigquery-validator',
    install_requires=[
        'google-cloud-bigquery',
        'Jinja2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.10'
)
