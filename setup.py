from setuptools import setup

setup(
    name = "adsy",
    version = "0.1.0",
    package_dir = {'': 'lib'},
    packages = ['adsy'],

    install_requires = [
        'pandas',
        'ipython',
        'ipdb',
        'matplotlib',
        'numpy',
    ],

    author = "Jean-Louis Fuchs",
    author_email = "ganwell@fangorn.ch",
    description = "Adsy - Python tools",
    license = "Modified BSD",
    long_description = """
* ipython notebook display tools (display.py)
  * display cursors and multidicts as tables
  * wrap and pretty print other data
* ipython notebook hide input (display.py)
  * nbconvert your ipython notebooks and hide the input
  * useful when sending notebooks to non-programmers
* helper to formulate queries as list comprehenions (iterator.py)
* Helpful tools for ipython notebooks (contains everything above)
  * Also contains a method to enable autoreload
  * A helper for automatic git bisect
* tools to enhance the look of matplotlib charts (plotenhance.py)""",
    keywords = "adfinis-sygroup ipython matplotlib pandas",
    url = "https://github.com/adfinis-sygroup/adsy-python",
    #download_url = "",
    #bugtrack_url = "https://github.com/adfinis-sygroup/adsy-python/issues",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Testing",
    ]
)
