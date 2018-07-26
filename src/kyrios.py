## Provisioning script
from packageManagerBash import packageManagerBash
from packageManagerHomebrew import packageManagerHomebrew
from packageManagerNpm import packageManagerNpm
from packageManagerIntrinsic import packageManagerIntrinsic
from packageManagerPip import packageManagerPip

import argparse
import glob
import logging
import os
import platform
import stdplus
import yaml

packageManagers = {
    'bash': packageManagerBash(),
    'homebrew': packageManagerHomebrew(),
    'intrinsic': packageManagerIntrinsic(),
    'npm' : packageManagerNpm(),
    'pip' : packageManagerPip()
}

def fatal(message):
    logging.exception(message)
    raise RuntimeError(message)

def readPackage(filename, context):
    """ Read a package definition into the context """
    packageMetadata = yaml.load(open(filename))
    key = os.path.splitext(os.path.basename(filename))[0]
    if not 'platforms' in packageMetadata:
        fatal("Package '{}' does not specify any platforms.".format(filename))

    context['packages'][key] = packageMetadata

def getInstallPlatform(context, package):
    installPlatform = context['simplifiedPlatform']
    if not installPlatform in  package['platforms']:
        installPlatform = 'generic'
    if not installPlatform in package['platforms']:
        fatal("Package '{}' does not support platform '{}'".format(packageName, context['simplifiedPlatform']))
    return installPlatform

def getPlatformConfig(context, package):
    installPlatform = getInstallPlatform(context, package)
    return package['platforms'][installPlatform]

def requirePackage(packageName, context, visited):
    """ Install a package if it isn't installed. """
    logging.debug("requirePackage('{}', context, {})".format(packageName, visited))

    if packageName in context['installedPackages']:
        return

    if packageName in visited:
        fatal("Cyclical dependency detected. '{}' is already in '{}'".format(packageName, visited))

    # Grab the package definition from the list of packages
    if not packageName in context['packages']:
        logging.warn("The package '{}' is required, but does not have a definition in the 'packages/' directory".format(packageName))
    package = context['packages'][packageName]

    # Read the platform-independent dependencies
    dependencies = []
    if 'dependencies' in package:
        dependencies.extend(package['dependencies'])

    platformConfig = getPlatformConfig(context,package)
    packageManagerName = platformConfig['packageManager']
    dependencies.append(packageManagerName)

    # Munge in the platform-dependent dependencies
    simplifiedPlatform = context['simplifiedPlatform']
    if 'platforms' in package and simplifiedPlatform in package['platforms'] and 'dependencies' in package['platforms'][simplifiedPlatform]:
        dependencies.extend(package['platforms'][simplifiedPlatform]['dependencies'])

    for dependency in dependencies:
        requirePackage(dependency, context, visited + [packageName])

    installPackage(packageName, package, context)

def installPackage(packageName, package, context):
    if packageName in context['installedPackages']:
        return

    platformConfig = getPlatformConfig(context,package)
    packageManagerName = platformConfig['packageManager']
    packageManager = packageManagers[packageManagerName]
    logging.debug("found packageManager: '{}': {}".format(packageManagerName, packageManager))

    packageManager.installPackage(packageName, package, context, platformConfig)
    context['installedPackages'].append(packageName)

def provision(filename, context):
    if not os.path.exists(filename):
        fatal("You do not have a profile configured at {}".format(filename))
    profile = yaml.load(open(filename))
    for package in profile['installPackages']:
        requirePackage(package, context, [])

def argument_parser(defaults):
    result = argparse.ArgumentParser(description='Kyrios: The Package Manager Manager')
    result.add_argument('-p', '--profile', dest='profileFilename', help='Profile Filename')
    result.set_defaults(**defaults)
    return result

def main():
    context = {
        'simplifiedPlatform': platform.system(),
        'packages': {},
        'installedPackages': ['intrinsic']
    }
    defaults = {
        'profileFilename' : os.path.expanduser('~/.kyrios/profile.yaml')
    }
    args = argument_parser(defaults).parse_args()

    packageCount = 0
    for filename in glob.iglob("packages/*.yaml"):
        packageCount += 1
        readPackage(filename, context)

    logging.debug("{} packages found".format(packageCount))

    provision(args.profileFilename, context)

if __name__ == "__main__":
    main()
