from setuptools import setup, find_packages

setup(
    name='github_user_activity',
    version='1.0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
        'click',
        'rich',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'github-activity=github_user_activity.cli:cli'
        ],
    },
    description='A CLI tool to display GitHub user activity',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
