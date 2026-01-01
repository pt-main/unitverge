import os
from setuptools import setup, Extension, find_packages
from pathlib import Path

print('==== Creating libs dir ====')
LIBS = Path.home() / 'BTXLIBS'
LIBS.mkdir(exist_ok=True)
print('==== Creating libs dir Success ====')

import stdlibs

for lib in stdlibs.libs.keys():
    with open(LIBS/f'{lib}.btx', 'w') as file:
        file.write(stdlibs.libs[lib])



__bx_version__ = '2.0'
__framework_verion__ = '1.2'

match __bx_version__:
    case '1.0':
        path = 'src/C-CORES/bx1/'
        bytex = Extension(
            name='untvgdev.core.bx1.UnitBytexCore',
            sources=[path + 'UnitBytexCore.c'],
        )
        config = Extension(
            name='untvgdev.core.bx1.UnitBytexDevConfig', 
            sources=[path + 'UnitBytexDevConfig.c'],
        )
        c_mod = [bytex, config]
    
    case '2.0':
        path = 'src/UnitVerge/Bytex/bx2/'
        basemem = Extension(
            name='BYTEX2_back',
            sources=[path + 'machine/BYTEX2_back.c'],
        )
        c_mod = [basemem]


setup(
    name='unitverge',
    author='Pt',
    author_email='kvantorium73.int@gmail.com',
    version=__framework_verion__,
    ext_modules=c_mod,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    description='A metaprogramming framework for code generation and DSL creation',
    url='https://github.com/pt-main/unitverge',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'btx2=btx_tool.btx2:main',
            'bytex=btx_tool.bytex:main'
        ]
    },
    options={
        'bdist_wheel': {
            'python_tag': 'cp314',
            'plat_name': 'manylinux2014_x86_64',
        }
    }
)
