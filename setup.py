from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README_PYPI.md").read_text(encoding="utf-8")

setuptools.setup(
    name="streamlit-advanced-audio",
    version="0.1.2",
    author="Keli Wen",
    author_email="pkuwkl@gmail.com",
    description="Advanced audio player component for Streamlit with waveform visualization and region selection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keli-wen/streamlit-advanced-audio",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=0.63",
        "numpy",
        "pandas",
        "requests",
        "soundfile",
    ],
    extras_require={
        "dev": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.48.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
        ]
    }
)
