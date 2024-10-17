from setuptools import setup, find_packages

setup(
    name='github_user_activity',
    version='0.3.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'github-activity=cli:cli'
        ],
    },
    install_requires=[
        'click',
        'rich'
    ]
)
