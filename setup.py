try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='memcacheinspector',
    version='0.1.0',
    packages=find_packages('src'),
	scripts = [
		'bin/mcinspect',
	]

    author='Jason Simeone',
    author_email='jay@classless.net',
    url='',
    description='Memcache Inspection Utility',
    long_description='',
	license='',
	keywords='memcache inspector dump',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
    ]

    package_dir={'' : 'src'},
)
