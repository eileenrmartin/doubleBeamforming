import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doublebeamforming", # Replace with your own username
    version="0.0.1",
    author="Eileen R. Martin",
    author_email="eileenrmartin@vt.edu",
    description="A package for traditional and new algorithms for ambient noise double beamforming transforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eileenrmartin/doubleBeamforming",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)