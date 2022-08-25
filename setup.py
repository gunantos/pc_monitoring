from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name='socket_monitoring',
    version='1.0.0',
    description='Monitoring computer realtime with socket',
    long_description=long_description,
    author='gunantos',
    author_email='gunanto.simamora@gmail.com',
    url='https://github.com/gunantos/socket-monitoring',
    license='MIT',
    keywords='monitoring, computer',
    python_requires=">=3.7, <4",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'requests',
        'socket',
        'pyspectator'],
    project_urls={
        "Bug Reports": "https://github.com/gunantos/socket-monitoring/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https: // github.com/gunantos/socket-monitoring",
    },
)
