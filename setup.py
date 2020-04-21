import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysurvecto",
    version="0.0.1",
    author="Eric Dodge, Jeenu Thomas",
    author_email="it@idinsight.org, Eric.Dodge@idinsight.org, Jeenu.Thomas@idinsight.org",
    description="Interacting with SurveyCTO using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IDinsight/surveycto-python/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)