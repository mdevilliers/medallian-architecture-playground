from setuptools import find_packages, setup

setup(
    name="rss_ingestion",
    packages=find_packages(exclude=["rss_ingestion_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-aws"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
