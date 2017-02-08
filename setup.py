from setuptools import setup

setup(
    name='load_guard_cog',
    version='0.1',
    packages=['load_guard_cog', 'load_guard_cog.modules', 'load_guard_cog.commands', 'load_guard_cog.recorders'],
    url='https://github.com/Rashitko/load_guard_cog',
    download_url='https://github.com/Rashitko/load_guard_cog/master/tarball/',
    license='MIT',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['up', 'psutil', 'pyyaml'],
    package_data={
        'load_guard_cog': ['load_guard_cog/registered_modules.yml']
    }
)
