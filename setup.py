DESCRIPTION = "A backend core utility library."

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Typing :: Typed
Operating System :: OS Independent
"""

INSTALL_REQUIREMENTS = """\
sqlalchemy>=1.4
marshmallow>=3.14
"""


def setup_pkg():
    import setuptools

    metadata = dict(
        name="nekoite-be-core",
        version="0.1.3",
        author="Nekoite",
        author_email="nekoite@rebuild.moe",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/nekoite/nekoite-be-core",
        classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
        python_requires=">=3.7",
        install_requires=[_f for _f in INSTALL_REQUIREMENTS.split("\n") if _f],
        package_dir={"": "src"},
        packages=setuptools.find_packages("src"),
    )

    setuptools.setup(**metadata)


if __name__ == "__main__":
    setup_pkg()
