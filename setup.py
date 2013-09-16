##------------------------------------------------------------
## DataPub - data publication application
##------------------------------------------------------------

import sys
from pkg_resources import normalize_path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1-alpha'

install_requires = [
    "Flask",
    #"Flask-RESTful",

    #"Flask-OpenID",  # Maybe in the future
    #"Flask-Login",  # This looks nice.. -> can we store users in graph too?
    #"Flask-SQLAlchemy",  # we use rdflib for this
    #"Flask-Restless",  # ?

    ## todo: we'd need a rdflib store backed by datapub API

    # "psycopg2",  # Only if using postgresql
    # "six",  # This is apparently needed, for py3k (py3k not supported yet)

    "rdflib>=4.0",
    "rdflib-sqlalchemy",
    #"rdflib-jsonld==0.1",
]

dependency_links = [
    'https://github.com/RDFLib/rdflib-sqlalchemy/archive/master.zip#egg=rdflib-sqlalchemy-dev',
    'git+https://github.com/RDFLib/rdflib-sqlalchemy.git@master#egg=rdflib-sqlalchemy-dev',
    #'git+https://github.com/RDFLib/rdflib-jsonld.git@master#egg=rdflib-jsonld-0.1',
]

tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--ignore=build',
            '--cov=datapub',
            '--cov-report=term-missing',
            '--pep8',
            '.']
        self.test_suite = True

    def run_tests(self):
        from pkg_resources import _namespace_packages
        import pytest

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and \
                getattr(self.distribution, 'use_2to3', False):
            module = self.test_args[-1].split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code..
            ei_cmd = self.get_finalized_command("egg_info")
            self.test_args = [normalize_path(ei_cmd.egg_base)]

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='DataPub',
    version=version,
    packages=find_packages(),
    url='',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='',
    long_description='',
    install_requires=install_requires,
    dependency_links=dependency_links,
    tests_require=tests_require,
    test_suite='datapub.tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'datapub = datapub.cli:run_from_command_line',
        ],
    },
    **extra
)
