import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topdownpygame",
    version="0.0.1",
    author="willieLjohnson",
    author_email="liwa.johnson@gmail.com",
    description="A modular pygame wrapper that adds ECS, procedural generation, cameras, and physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willieljohnson/pygg/",
    project_urls={
        "Bug Tracker": "https://github.com/willieljohnson/pygg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)