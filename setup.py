from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="cxc",
    version="1.0.0",
    description="CodeX Core, Ai Tools For Terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["cxc", "chat", "colors", "downloader", "mpx", "config_loader"],
    include_package_data=True,
    install_requires=["requests", "textual", "yt-dlp", "rapidfuzz"],
    entry_points={"console_scripts": ["cxc=cxc:main"]},
    url="https://github.com/XyrionMD/Cxc",
    author="Xyrion",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

