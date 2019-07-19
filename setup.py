import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loopimer",
    version="1.0.1",
    author="Rouzbeh Afrasiabi",
    author_email="rouzbeh.afrasiabi@gmail.com",
    description="Package for time-controlled consecutive execution of a  function using threading.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rouzbeh-afrasiabi/loopimer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)