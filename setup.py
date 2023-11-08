import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

for e in ["utf-8", "utf-8-sig", "utf16"]:
    try:
        requirements_list = [line.strip() 
                     for line in open('requirements.txt', encoding=e) 
                     if line.strip()]
        break
    except:
        pass


setuptools.setup(
    name='gnarrator',
    version='0.9.4',
    python_requires='>=3.9.0',
    author='Arnau Castelalno',
    author_email='arcascb2001@gmail.com',
    description='A screen reading accessibility tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/arcb01/g-narrator',
    packages=setuptools.find_packages(),
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
   ],
   entry_points={
       'console_scripts': [
            'gnarrator = gnarrator.__main__:_main'
       ]
    },
    install_requires=requirements_list
) 
