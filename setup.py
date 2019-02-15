from setuptools import setup

packages = [
    'directories'
]

install_requires = [
    'persistentdatatools >= 2.2.7, < 3',
    'pyyaml == 4.2b4',
    'pyreadline ==2.1;sys_platform=="win32"',
]

tests_require = [
    'pytest',
]

setup(
    name='directories',
    version='1.0.7',
    python_requires='~=3.3',
    description='This is a class that helps make dealing with your scripts directories easier',
    keywords='dir class directories yml',
    url='https://github.com/btr1975/directories',
    author='Benjamin P. Trachtenberg',
    author_email='e_ben_75-python@yahoo.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    test_suite='pytest',
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
