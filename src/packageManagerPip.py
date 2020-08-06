
from packageManager import packageManager
import logging
import subprocess

class packageManagerPip(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        managedPackageName = platformConfig['packageName']
        pip = platformConfig.get('pipCommand','pip')
        command = [pip, "show", managedPackageName]
        print(command)
        result = subprocess.run(command)
        return result.returncode is 0

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package {} is already installed".format(packageName))
            return
        logging.debug("{}: installing package {}".format(self.__class__.__name__, packageName))
        managedPackageName = platformConfig['packageName']
        pip = platformConfig.get('pipCommand','pip')
        command = [pip, "install", managedPackageName]
        subprocess.run(command, check=True)