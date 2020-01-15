import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='freshsalessdk',
    version='0.0.5',
    author='Siva Narayanan',
    author_email='siva@fyle.in',
    description='Python SDK for accessing Freshsales',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['freshsales', 'api', 'python', 'sdk'],
    url='https://github.com/fylein/freshsales-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
