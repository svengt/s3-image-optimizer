"""
S3 Image Optimizer optimizes all images found in an Amazon S3 bucket.
"""
from setuptools import find_packages, setup

dependencies = [
    'click==5.1',
    'boto==2.38.0',
]

setup(
    name='s3-image-optimizer',
    version='0.1.0',
    url='https://github.com/svengt/s3-image-optimizer',
    download_url='https://github.com/svengt/s3-image-optimizer/tarball/0.1.0',
    license='BSD',
    author='Sven Groot',
    author_email='sven@mediamoose.nl',
    description='S3 Image Optimizer optimizes all images found in an Amazon S3 bucket.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            's3-optimize = s3_image_optimizer.cli:main',
        ],
    },
    keywords=['s3', 'image', 'optimization', 'amazon', 'aws', 'boto'],
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
