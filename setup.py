from setuptools import setup, find_packages

setup(
    name='pybot-fabric',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages("src"),
    package_dir={'': 'src'},
    url='',
    license='',
    author='Eric Pascual',
    author_email='eric@pobot.org',
    description='Common fabric tasks',
)
