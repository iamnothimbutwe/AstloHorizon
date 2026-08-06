# ---------------------------------------------------------
# Copyright (c) 2026 Mark. All rights reserved.
# Unauthorized copying of this file, via any medium, is
# strictly prohibited. Written by Mark (iamnothimbutwe) on Github.
# ---------------------------------------------------------

from setuptools import setup, find_packages


setup(
    name = 'astlohorizons',
    version = 'v0.1.1',
    packages=find_packages(),
    install_requires = ['rich','astlo>=v10.350.500','click','skyfield'],
    include_package_data = True,
    entry_points={
        "console_scripts": [
            "astlohorizons = asho.main:iam",
            ],
    },
    python_requires=">=3.10",                                             author="maxharia/@iamnothimbutwe Github and Gitlab",
    # author_email="markmacgh@gmail.com/hecateare@gmail.com", shouod add the entity email
    description="an optional plugin for astlo that utilizes ephemeris data from NASA-JPL spice kernels. its function is to help astlo track  moons and stars.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamnothimbutwe/AstloHorizons",
    license="Copyright (c). All rights reserved",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: COPYRIGHT",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Astronomy :: Astrophysics",
    ],
)


