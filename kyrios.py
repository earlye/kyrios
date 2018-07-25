## Provisioning script
from __future__ import print_function

import argparse
import glob
import os
import platform
import stdplus
import yaml

from pprint import pprint

class packageManager:
    pass

class packageManagerShell(packageManager):
    def isInstalled(self,packageName,package,context,platformConfig):
        if 'isInstalled' in platformConfig:
            command = platformConfig['isInstalled']
            result = stdplus.run(command,throwOnNonZero = False)
            return result is 0
        pass

    def installPackage(self,packageName,package,context,platformConfig):
        if self.isInstalled(packageName,package,context,platformConfig):
            print("DEBUG: package '{}' is installed".format(packageName))
            return
        print("DEBUG: packageManagerShell: installing package '{}'".format(packageName))
        command = platformConfig['installCommand']
        if command:
            stdplus.run(command)

class packageManagerHomebrew(packageManager):
    def isInstalled(self,packageName,package,context,platformConfig):
        managedPackageName = platformConfig['packageName']
        command = "brew ls --versions '{}' > /dev/null".format(managedPackageName)
        result = stdplus.run(command,throwOnNonZero = False)
        return result is 0

    def installPackage(self,packageName,package,context,platformConfig):
        if self.isInstalled(packageName,package,context,platformConfig):
            print("DEBUG: package '{}' is installed".format(packageName))
            return
        print("DEBUG: packageManagerHomebrew: installing package '{}'".format(packageName))
        managedPackageName = platformConfig['packageName']
        command = "brew install '{}'".format(managedPackageName)
        stdplus.run(command)

class packageManagerNpm(packageManager):
    def isInstalled(self,packageName,package,context,platformConfig):
        managedPackageName = platformConfig['packageName']
        command = "npm list -g | grep '{}' > /dev/null".format(managedPackageName)
        result = stdplus.run(command,throwOnNonZero = False)
        return result is 0

    def installPackage(self,packageName,package,context,platformConfig):
        if self.isInstalled(packageName,package,context,platformConfig):
            print("DEBUG: package '{}' is installed".format(packageName))
            return
        print("DEBUG: packageManagerNpm: installing package '{}'".format(packageName))
        managedPackageName = platformConfig['packageName']
        command = "npm install -g '{}'".format(managedPackageName)
        stdplus.run(command)

class packageManagerPip(packageManager):
    def isInstalled(self,packageName,package,context,platformConfig):
        managedPackageName = platformConfig['packageName']
        command = "pip show '{}' > /dev/null".format(managedPackageName)
        result = stdplus.run(command,throwOnNonZero = False)
        return result is 0

    def installPackage(self,packageName,package,context,platformConfig):
        if self.isInstalled(packageName,package,context,platformConfig):
            print("DEBUG: package '{}' is installed".format(packageName))
            return
        print("DEBUG: packageManagerPip: installing package '{}'".format(packageName))
        managedPackageName = platformConfig['packageName']
        command = "pip install '{}'".format(managedPackageName)
        stdplus.run(command)

packageManagers = {
    'shell': packageManagerShell(),
    'homebrew': packageManagerHomebrew(),
    'npm' : packageManagerNpm(),
    'pip' : packageManagerPip()
}

def fatal(message):
    print("ERROR: {}".format(message))
    raise RuntimeError(message)

def readPackage(filename,context):
    """ Read a package definition into the context """
    packageMetadata = yaml.load(open(filename))
    key = os.path.splitext(os.path.basename(filename))[0]
    if not 'platforms' in packageMetadata:
        fatal("Package '{}' does not specify any platforms.".format(filename))

    context['packages'][key] = packageMetadata

def requirePackage(packageName,context,visited):
    """ Install a package if it isn't installed. """
    print("DEBUG: requirePackage('{}',context,{})".format(packageName,visited))

    if packageName in visited:
        fatal("Cyclical dependency detected. '{}' is already in '{}'".format(packageName,visited))

    # Grab the package definition from the list of packages
    if not packageName in context['packages']:
        print("The package '{}' is required, but does not have a definition in the 'packages/' directory".format(packageName))
    package = context['packages'][packageName]

    # Read the platform-independent dependencies
    dependencies = []
    if 'dependencies' in package:
        dependencies.extend(package['dependencies'])

    # Munge in the platform-dependent dependencies
    simplifiedPlatform = context['simplifiedPlatform']
    if 'platforms' in package and simplifiedPlatform in package['platforms'] and 'dependencies' in package['platforms'][simplifiedPlatform]:
        dependencies.extend(package['platforms'][simplifiedPlatform]['dependencies'])

    for dependency in dependencies:
        requirePackage(dependency,context,visited + [packageName])

    installPackage(packageName,package,context)

def installPackage(packageName,package,context):
    if packageName in context['installedPackages']:
        return

    print("DEBUG: need to check if package '{}' is installed".format(packageName))
    simplifiedPlatform = context['simplifiedPlatform']
    installPlatform = simplifiedPlatform
    if not installPlatform in  package['platforms']:
        installPlatform = 'generic'
    if not installPlatform in package['platforms']:
        fatal("Package '{}' does not support platform '{}'".format(packageName,simplifiedPlatform))

    platformConfig=package['platforms'][installPlatform]
    print("DEBUG: mapped platform '{}' to '{}'".format(simplifiedPlatform,platformConfig))

    packageManagerName=platformConfig['packageManager']
    packageManager = packageManagers[packageManagerName]
    print("DEBUG: found packageManager: '{}': {}".format(packageManagerName,packageManager))

    packageManager.installPackage(packageName,package,context,platformConfig)

def provision(filename,context):
    profile = yaml.load(open(filename))
    for package in profile['installPackages']:
        requirePackage(package,context,[])

def main():
    context={
        'simplifiedPlatform': platform.system(),
        'packages': {},
        'installedPackages': []
    }

    packageCount = 0
    for filename in glob.iglob("packages/*.yaml"):
        packageCount+=1
        readPackage(filename,context)

    print("DEBUG: {} packages found".format(packageCount))

    ## TODO: select profile more intelligently than this hard-coding.
    provision(os.path.expanduser("~/.kyrios/profile.yaml"),context)

if __name__=="__main__":
    main()
