from setuptools import setup, find_packages

setup(
    name="flowise",
    version="1.0.1",
    description="Flowise SDK for Python to interact with the Flowise API.",
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
