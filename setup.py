from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='flexdict',
    version='0.0.1a1',
    author='Berkay Öztürk',
    author_email='info@berkayozturk.net',
    description='Python dict with automatic and arbitrary levels of nesting along with additional utility methods.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ozturkberkay/flexdict',
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    python_requires='>=2.7',
    keywords='automatic arbitrary dict nesting',
    project_urls={
        'Bug Reports': 'https://github.com/ozturkberkay/FlexDict/issues',
        'Source': 'https://github.com/ozturkberkay/FlexDict'
    },
)
