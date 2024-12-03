# GLYCAM Extensible Modeling Scripts (GEMS)

This code serves as a convenient interface to the molecular modeling code
in the [Glycam Molecular Modeling Library](https://github.com/GLYCAM-Web/gmml). 
The interface is used by [GLYCAM-Web](https://glycam.org). Use of
this interface ensures that the services provided by the website give
exactly the same results as you would get using GEMS on the command line. 
The general concept is that a JSON file is used as input to the bin/delegate script.

# Funding Sources

GLYCAM-Web is made possible by our [funders](https://github.com/GLYCAM-Web/website/blob/master/funding.md)

# Installing GEMS (GLYCAM Extensible Modeling Script)

[Prerequisites](#prerequisites)  
[Obtaining the software](#obtaining-the-software)  
[Compiling and Installing](#compiling-and-installing)  
[Testing the Installation](#testing-the-installation)  
[Example Use](#example-use)  
[Documentation](#documentation)  

## Prerequisites

In order to install GEMS, you will need to have the following software available on your system: 

* `openssl` 
* `git` 
* `python3.9`
* `python3.9-dev` (you need the Python header files for your Linux distro, which may not be part of your existing Python package)
* `swig` (Version >= 4.0.2)
* Kernel headers (the source code for the Linux kernel, which may not be installed on your system)
* `cmake` (Version >= 3.13.4)
* `boost`

**NOTE** - installing some prerequisites may require `root` access. Also swig must be installed from [their website](https://www.swig.org/download.html)

Please note that in order to use GEMS you must also have GMML installed and compiled. Most of the above packages are needed for compiling GMML

Installation instructions will vary according to the package management software your distro uses.  If you use Ubuntu or any other Debian based system, you should be able to use a command like this:

```bash
sudo apt-get install openssl git python3.9 python3.9-dev build-essential cmake libboost-all-dev 
```
For other Linux distros, please follow the instructions for the package management software included with your system. 

---

## Obtaining the software

Once you have installed the prerequisites, you can install the GEMS software. 

**NOTE** - installing GEMS **does not** require `root` access. We do not recommend installing GEMS or GMML as root. 

Change to the directory where you will install GEMS, and clone the GEMS repo from Github: 

`git clone https://github.com/GLYCAM-Web/gems.git`

This will create a *`gems`* directory. Change to the *`gems`* directory, and clone the GMML repos from Github: 

```bash
cd gems/
git clone https://github.com/GLYCAM-Web/gmml.git
git clone https://github.com/GLYCAM-Web/gmml2.git
```
Both repos are currently required. 

---

## Compiling and Installing

To compile the software, make sure you are still in the *`gems`* directory: 

```bash
pwd
/gems
```

Set your **`PYTHON_HOME`** environment variable to the location of the `Python.h` file for your Python version. For Ubuntu, use something like one of the following: 

`export PYTHON_HOME=/usr/include/python3.9`   
or   
`setenv PYTHON_HOME /usr/include/python3.9`  

Make sure to use the correct path to your Python version, and the correct version of Python. 
For other Linux distros, please follow the instructions to set environment variables specific to your system. 

There are a handful of ways to use more processors while compiling:

```bash
.../gems$ make.sh -j 8
``` 

This will compile GMML and GMML2 with 8 cores.

## Testing the Installation

Make sure you are still in the *`gems`* directory, and run the following command to test the installation: 

Please note that there are tests within the `tests/` directory but many will fail because they require you to have a stack running that can handle DNS because we submit a JSON request with one of the tests (specifically test 008). These tests are expected to fail if you are only running GEMS. 

Make sure you are still in the *`gems`* directory, and run the following command, which is all on one line:   
python3 bin/AmberMDPrep.py tests/inputs/016.AmberMDPrep.4mbzEdit.pdb
You should see a lot of info that ends:
Disulphide bonds:
Chain terminations:
A  |  25  |  NH3+  |  301  |  CO2-
B  |  25  |  NH3+  |  299  |  CO2-
C  |  25  |  NH3+  |  299  |  CO2-
D  |  26  |  NH3+  |  299  |  CO2-
E  |  25  |  NH3+  |  301  |  CO2-
F  |  25  |  NH3+  |  298  |  CO2-
G  |  25  |  NH3+  |  298  |  CO2-
H  |  25  |  NH3+  |  298  |  CO2-
I  |  25  |  NH3+  |  299  |  CO2-
J  |  24  |  NH3+  |  300  |  CO2-
We made it to the end. Congratulations!

