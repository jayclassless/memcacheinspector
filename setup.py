try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='memcacheinspector',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
	scripts = [
		'bin/mcinspect',
	],
    install_requires='python-memcached',

    author='Jason Simeone',
    author_email='jay@classless.net',
    url='',
    description='Memcache Inspection Utility',
    long_description='',
	license='',
	keywords='memcache inspector dump search grep',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
