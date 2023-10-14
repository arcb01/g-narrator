import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements_list = [line.strip() 
                     for line in open('requirements.txt', encoding="utf-16") 
                     if line.strip()]

setuptools.setup(
    name='garrator',
    version='0.3.0',
    python_requires='>=3.9.0',
    author='Arnau Castelalno',
    author_email='arcascb2001@gmail.com',
    description='A screen reading accessibility tool for videogames',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/arcb01/gaming-narrator',
    packages=setuptools.find_packages(),
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
   ],
   entry_points={
       'console_scripts': [
            'garrator = garrator.run:main'
       ]
    },
    install_requires=requirements_list
) 