import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="college-football",
    version="0.0.5",
    author="Zoe Surma",
    author_email="zdawg1022@gmail.com",
    description="A college football analysis package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zsurma/college-football",
    project_urls={
        "Bug Tracker": "https://github.com/zsurma/college-football/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8"
)
