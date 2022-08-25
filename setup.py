from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name='pc_monitoring',
    version='0.0.5',
    description='Monitoring computer realtime with socket',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='gunantos',
    author_email='gunanto.simamora@gmail.com',
    url='https://github.com/gunantos/pc_monitoring',
    license='MIT',
    keywords='monitoring, computer',
    python_requires=">=3.7, <4",
    package_dir={"": "src"},
    py_modules=["pc_monitoring"],
    packages=find_packages(where="src"),
    install_requires=[
        'requests',
        'pyspectator'],
    project_urls={
        "Bug Reports": "https://github.com/gunantos/pc_monitoring/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https: // github.com/gunantos/pc_monitoring",
    },
)
