import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='memcacheinspector',
    version='0.2.1',
    packages=find_packages(exclude=['tests']),
	scripts = [
		'bin/mcinspect',
	],
    install_requires='python-memcached',
    author='Jason Simeone',
    author_email='jay@classless.net',
    url='https://github.com/jayclassless/memcacheinspector',
    description='Memcache Inspection Module and Command-Line Utility',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
	license='MIT',
	keywords='memcache memcached inspector list dump export search grep keys',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
