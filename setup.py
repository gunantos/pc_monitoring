import sys
import platform
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """
    Test-runner
    """

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def __init__(self, *args, **kwargs):
        super(PyTest, self).__init__(*args, **kwargs)
        self.pytest_args = None
        self.test_suite = None

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = list()

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = list()
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        err_no = pytest.main(self.pytest_args)
        sys.exit(err_no)


def main():
    # Check python version
    if sys.version_info < (3, 0, 0):
        sys.stderr.write(
            'You need python 3.0 or later to run this script!' + os.linesep
        )
        exit(1)
    # Generate requires
    if 'Windows' in platform.system():
        requirements_file = 'windows.txt'
    elif 'Linux' in platform.system():
        requirements_file = 'linux.txt'
    else:
        requirements_file = 'default.txt'
    requirements_file = os.path.join('requirements', requirements_file)
    with open(requirements_file) as requirements_reader:
        requires = requirements_reader.read().splitlines()
    # Get package description
    with open('README.MD') as readme_reader:
        long_description = readme_reader.read()
    # Describe installer
    settings = {
        'name': 'pc_monitoring',
        'version': '0.0.6',
        'author': 'gunantos',
        'author_email': 'gunanto.simamora@gmail.com',
        'maintainer': 'gunantos',
        'maintainer_email': 'gunanto.simamora@gmail.com',
        'packages': ['pc_monitoring'],
        'url': 'https://github.com/gunantos/pc_monitoring',
        'download_url': 'https://github.com/gunantos/pc_monitoring/releases',
        'license': 'MIT',
        'description': 'pc_monitoring is a Python cross-platform tool for '
                       'monitoring OS resources.',
        'long_description': long_description,
        'install_requires': requires,
        'keywords': [
            'pc_monitoring', 'monitoring',
            'monitoring', 'tool',
            'statistic', 'stats',
            'computer', 'pc', 'server',
            'mem', 'memory',
            'network', 'net', 'io',
            'processor', 'cpu',
            'hdd', 'hard', 'disk', 'drive'
        ],
        'platforms': 'Platform Independent',
        'package_data': {
            'pc_monitoring': ['LICENSE', 'README.MD']
        },
        'scripts': ['console.py'],
        'tests_require': ['pytest>=2.6.2'],
        'cmdclass': {'test': PyTest},
        'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: C',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: System :: Benchmark',
            'Topic :: System :: Hardware',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
        ],
    }
    setup(**settings)


if __name__ == '__main__':
    main()
