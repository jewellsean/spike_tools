import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spike_tools-jewellsean", # Replace with your own username
    version="0.0.2",
    author="Sean Jewell",
    author_email="swjewell@uw.edu",
    description="Tools for spike estimation via L0 optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
