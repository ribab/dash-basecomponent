from setuptools import setup, find_packages

setup(
    name='dash_basecomponent',
    version='0.1.0',
    description='A base component library for Dash applications',
    author='Richard Barella Jr.',
    author_email='codingwithricky@gmail.com',
    url='https://github.com/yourusername/dash_basecomponent',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=[
        'dash>=2.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    # python_requires='>=3.6',
    include_package_data=True,
)
