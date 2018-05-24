
from setuptools import setup
from setuptools import find_packages


long_description = (
    "A set of MKDocs plugins to build awesome xRally documentation."
)


def read(filename):
    with open(filename) as f:
        return [l for l in f.readlines() if l and not l.startswith("#")]


setup(
    name="xrally_docs_tools",
    version="777",
    url="https://github.com/xrally/xrally-docs",
    license="Apache",
    description="Plugins for MKDocs.",
    long_description=long_description,
    author="xRally team",
    author_email='noreply-sorry@xrally.org',
    packages=find_packages(),
    install_requires=read("./requirements.txt"),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
)
