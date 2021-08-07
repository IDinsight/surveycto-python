import setuptools
import os
import io

dir_path = os.path.abspath(os.path.dirname(__file__))
long_description = io.open(os.path.join(dir_path, 'README.rst'), encoding='utf-8').read()

setuptools.setup(
    name="pysurveycto",
    version="0.0.12",
    author="Eric Dodge, Jeenu Thomas",
    author_email="it@idinsight.org, Eric.Dodge@idinsight.org, Jeenu.Thomas@idinsight.org",
    description="Interacting with SurveyCTO using Python",
    long_description=long_description,
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