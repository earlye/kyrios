
from packageManager import packageManager
import logging
import subprocess

class packageManagerPip(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        managedPackageName = platformConfig['packageName']
        pip = platformConfig.get('pipCommand','pip')
        command = "{} show {}".format(pip,managedPackageName)
        print(command)
        result = subprocess.run(command.split())
        return result.returncode is 0

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package {} is already installed".format(packageName))
            return
        logging.debug("{}: installing package {}".format(self.__class__.__name__, packageName))
        managedPackageName = platformConfig['packageName']
        pip = platformConfig.get('pipCommand','pip')
        command = "{} install {}".format(pip,managedPackageName)
        result = subprocess.run(command.split())
        if result.returncode != 0:
            raise Exception(result.stderr)