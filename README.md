## Required Dependencies
- [Python](https://www.python.org/downloads/) (v3.11.7 recommended)
- [git](https://git-scm.com/downloads)
  
## Steps to setup
- Clone this repository using <br>`git clone https://github.com/Nisarg851/HumberChatbotBackend.git`
- Move into project folder
- run `pip install -r requirements.txt` to install all the required dependencies.
- run `fastapi run dev` to run the application in developer mode.
  
## Errors you may encounter
* <code style="color:red">ModuleNotFoundError: No module named 'distutils'</code>
  * The error indicates that Python is unable to find the distutils module, which is essential for package installation and management. This issue often arises due to changes in Python versions or environment configurations.
    * `distutils` is now part of the `setuptools` package. Try updating setuptools to the latest version by run the following command:<br> 
    `pip install --upgrade setuptools`
* <code style="color:red">AttributeError: module 'pkgutil' has no attribute 'ImpImporter'. Did you mean: 'zipimporter'?</code>
  * This error points to an inconsistency or potential issue with the pkgutil module, another standard library module used for package management.

  * **Option 1:** Upgrade pip <br> 
    `python -m pip install --upgrade pip`

  * **Option 2:** These packages are fundamental for Python package management. Try reinstalling them:<br>
  `python -m pip install --force-reinstall setuptools wheel`
    * now re-install the dependencies again with: <br>
    `pip install -r requirements.txt`

<br>

  > If the problem persists, try out different versions of dependencies in the **requirements.txt** file or install the dependencies manually.
 
