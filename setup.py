from setuptools import setup, find_packages

setup(
    name="ytdownloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "yt-dlp"
    ],
    entry_points={
        'console_scripts': [
            'ytdownloader = ytdownloader.main:main',
        ],
    },
    author="Your Name",
    description="A CLI tool to download and trim YouTube videos easily.",
    python_requires='>=3.7',
)
