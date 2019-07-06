import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyucum",
    version="0.1.2",
    author="Sam Tomioka",
    author_email="stomioka@gmail.com",
    description="Python library for using UCUM APIs to verify CDISC SDTM.LB and ADaM.ADLB",
    keywords='SDTM,ADaM, LB, ADLB, UCUM',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE',
    include_package_data=True,
    install_requires=[
    'numpy>=1.15.0',
    'pandas>=0.23.0',
    'tqdm4>=4.32.2',
    'seaborn>=0.9.0',
    'matplotlib>=3.1.1'],
    url='https://github.com/stomioka/ucum',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ],
)
