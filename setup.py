from setuptools import setup, find_packages


setup(
    name='flowroute-messaging-python',
    version='0.0.0',
    license='MIT',
    description='Flowroute\'s Messaging API',
    author='Flowroute Developers',
    author_email='developer@flowroute.com',
    url='https://github.com/flowroute/flowroute-messaging-python',
    packages=find_packages('.'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    keywords=[
        'messaging', 'sms', 'telephony', 'sip', 'api'
    ],
    install_requires=[
        'Unirest',
        'jsonpickle',
        'poster',
    ],
)
