import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyucum",
    version="0.1.0",
    author="Sam Tomioka",
    author_email="stomioka@gmail.com",
    description="Python library for using UCUM APIs to verify CDISC LB and ADLB",
    keywords='SDTM,ADaM, LB, ADLB, UCUM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE',
    include_package_data=True,
    install_requires=['setuptools', 'numpy','pandas','tqdm ','seaborn ','matplotlib'],
    url='https://github.com/stomioka/ucum',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ],
)
