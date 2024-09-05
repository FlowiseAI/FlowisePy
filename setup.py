from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="flowise",
    version="1.0.2",
    description="Flowise SDK for Python to interact with the Flowise API.",
    long_description=long_description,  # Use README.md as the long description
    long_description_content_type='text/markdown',  # This specifies the format
    author="Henry Heng",
    author_email="support@flowiseai.com",
    url="https://github.com/FlowiseAI/FlowisePy",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
