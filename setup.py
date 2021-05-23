import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='powerline-k8s',
    description='A Powerline segment for showing the active Kubernetes context and namespace',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.0',
    keywords='powerline k8s',
    license='MIT',
    author='Jordan Duabe',
    author_email='jordan.duabe@gmail.com',
    url='https://github.com/j4ckofalltrades/powerline-k8s',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Terminals'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
