import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRED_PACKAGES = [
    'datasketch>=1.4.3,<1.5.0', 'requests===2.20.1', 'pythainlp===2.0.6'
]

setuptools.setup(
    name="sixecho",
    version="0.2.7",
    author="six.network",
    author_email="dev-lead@six.network",
    description="digital contents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thesixnetwork/SIXEcho",
    packages=setuptools.find_packages(),
    install_requires=REQUIRED_PACKAGES,
    license='MIT',
    test_suite='nose.collector',
    tests_require=['nose'],
)
