"""
 A cli tool too launch, manage and use ethereum client on the cloud
"""
import os
import sys

import re
from setuptools import find_packages, setup


def find_version():
    with open('ethcloud/constants.py') as fl:
        content = fl.read()
        version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                                  content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


version = find_version()
dependencies = ['click', 'ansible', 'PyYaml', 'boto3', 'attrdict']

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push origin master --tags")
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()


setup(
    name='ethcloud',
    version=version,
    url='https://github.com/kgritesh/ethcloud',
    license='MIT',
    author='Ritesh Kadmawala',
    author_email='k.g.ritesh@gmail.com',
    description=' A cli tool too launch, manage and use ethereum client on the cloud',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'ethcloud = ethcloud:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
