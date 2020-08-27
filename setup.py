from setuptools import setup

setup(
    name='hisha',
    url='https://github.com/shunjuu/Hisha',
    author='Kyrielight',
    packages=['hisha'],
    install_requires=[
        'ayumi @ git+https://github.com/shunjuu/Ayumi',
        'deprecated',
        'requests',
    ],
    version='0.1',
    license='MIT',
    description='Anilist Data Fetcher.'
)