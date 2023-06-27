from setuptools import setup, find_packages


with open('README.md') as r:
    with open('LiCENSE') as lic:
        readme = r.read()
        license = lic.read()

setup(
    name='wolftrader',
    version='0.0.1',
    description='Very own trader bot, WIP',
    author='Nicolas Nunez',
    author_email='nicolasnunezromay@gmail.com',
    long_description=readme,
    license=license,
    url='',
    packages=find_packages(exclude=['docs','tests']),
    entry_points={
        'console_scripts': ['wolfmine=cli:miner',
                            'wolfmail=cli:notifier',
                            'wolfprocess=cli:processor',
                            'wolftrade=cli:trader']
    },
    classifiers=['Prog Lang - Python - 3.6']
)

