from setuptools import setup, find_packages

setup(
    name='github_user_activity',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'rich',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'github-activity=cli:cli'
        ],
    },
    description='A CLI tool to display GitHub user activity',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
