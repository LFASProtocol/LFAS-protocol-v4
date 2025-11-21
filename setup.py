from setuptools import setup, find_packages

setup(
    name="lfas-protocol",
    version="4.0.0",
    packages=find_packages(),
    install_requires=[
        "lxml>=4.9.0",
        "requests>=2.31.0"
    ],
    author="Mehmet Bagbozan",
    author_email="lfasprotocol@outlook.com",
    description="Logical Framework for AI Safety - Protecting Vulnerable Users",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LFASProtocol/LFAS-protocol-v4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
)
