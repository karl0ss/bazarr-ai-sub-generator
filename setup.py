from setuptools import setup, find_packages

setup(
    version="1.0",
    name="bazarr-ai-sub-generator",
    packages=find_packages(),
    py_modules=["bazarr-ai-sub-generator"],
    author="Karl Hudgell",
    install_requires=[
        'faster-whisper',
        'tqdm',
        'ffmpeg-python'
    ],
    description="Automatically generate and embed subtitles into your videos",
    entry_points={
        'console_scripts': ['bazarr-ai-sub-generator=bazarr-ai-sub-generator.cli:main'],
    },
    include_package_data=True,
)
