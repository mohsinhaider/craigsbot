import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="craigsbot",
    version="0.0.1",
    description="Craigslist web scraper for sending notifications about new listings",
    author="Mohsin Haider",
    author_email="github@mohsinhaider.com",
    url="https://github.com/mohsinhaider/craigsbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    license="MIT",
    keywords=["craigslist", "scraper", "twilio"],
    install_requires=[
        "beautifulsoup4==4.9.3",
        "mongoengine==0.23.0",
        "python-dotenv==0.17.1",
        "requests==2.25.1",
        "Shapely==1.7.1",
        "twilio==6.57.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
)