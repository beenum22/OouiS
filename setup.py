from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='Orion',
	version='1.0',
	description='Revolution towards a new flexible OvS API',
	long_description=readme(),
	url='http://github.com/beenum22/Orion',
	author='Muneeb Ahmad',
	author_email='muneeb.gandapur@gmail.com',
	entry_points = {
		'console_scripts': ['Orion=Orion.main:main']
	},
	packages=setuptools.find_packages(),
	#install_requires=[
	#	'pycrypto', 'ipaddress'
	#	],
	zip_safe=False)

