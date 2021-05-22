from setuptools import setup

setup(
    name='powerline-k8s',
    description='A Powerline segment for showing the active Kubernetes context and namespace',
    version='1.0.0',
    keywords='powerline k8s',
    license='MIT',
    author='Jordan Duabe',
    author_email='jordan.duabe@gmail.com',
    url='https://github.com/j4ckofalltrades/powerline-k8s',
    packages=['powerline_k8s'],
    install_requires=['powerline-status', 'kubernetes'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ]
)
