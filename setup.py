import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysurveycto",
    version="0.0.4",
    author="Eric Dodge, Jeenu Thomas",
    author_email="it@idinsight.org, Eric.Dodge@idinsight.org, Jeenu.Thomas@idinsight.org",
    description="Interacting with SurveyCTO using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IDinsight/surveycto-python/",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests>=2.0.0',
          'urllib3>=1.21.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)