from setuptools import setup, find_packages

setup(
    name='github_user_activity',
    version='0.3.5',
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
)
