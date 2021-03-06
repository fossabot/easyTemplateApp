#!/usr/bin/env python3

import sys, os
import BasicFunctions

# FUNCTIONS

def printSysPath():
    for path in sys.path:
        if path:
            print(path)


def upgradePip():
    message = "upgrade PIP"
    try:
        BasicFunctions.run('python', '-m', 'pip', 'install', '--upgrade', 'pip')
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def installFromGitE(owner, repo, branch, egg):
    url = "git://github.com/{0}/{1}.git@{2}#egg={3}".format(owner, repo, branch, egg)
    message = "install from '{}'".format(url)
    try:
        BasicFunctions.run('pip', 'install', '-e', url, exit_on_error=False)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        # sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def installFromGit(owner, repo, branch):
    url = "https://github.com/{0}/{1}/archive/{2}.zip".format(owner, repo, branch)
    message = "install from '{}'".format(url)
    try:
        BasicFunctions.run('pip', 'install', url)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def install(*packages):
    for package in packages:
        message = "install '{}'".format(package)
        try:
            BasicFunctions.run('pip', 'install', package)
        except Exception as exception:
            BasicFunctions.printFailMessage(message, exception)
            sys.exit()
        else:
            BasicFunctions.printSuccessMessage(message)

def fixDictdifferNumpy():
    from_str = "    LIST_TYPES += (numpy.ndarray, )"
    to_str = (from_str + os.linesep + os.linesep +
        "#Temporary fix for PyInstaller assuming numpy is installed" + os.linesep +
        "HAS_NUMPY = True" + os.linesep +
        "import numpy" + os.linesep +
        "LIST_TYPES += (numpy.ndarray, )")
    import Project
    config = Project.Config()
    dictdiffer_init_py_path = os.path.join(config['pyinstaller']['lib_path']['dictdiffer'], '__init__.py')
    with open(dictdiffer_init_py_path, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(from_str, to_str)
    with open(dictdiffer_init_py_path, 'w') as file:
        file.write(filedata)

# MAIN

if __name__ == '__main__':
    BasicFunctions.printTitle('Upgrade PIP and install packages')

    upgradePip()

    #installFromGit(owner='ikibalin', repo='cryspy', branch='transition-to-version-0.2')
    #installFromGit(owner='easyDiffraction', repo='easyInterface', branch='polarisation_start') # Until master branch is uploaded to PIP

    install(
        'PySide2>=5.14.1',
    )

    #if BasicFunctions.osName() == 'windows':
    #    install('pypiwin32')

    #fixDictdifferNumpy()
