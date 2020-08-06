
from packageManager import packageManager
import logging
import subprocess

class packageManagerBash(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        if 'isInstalled' in platformConfig:
            command = platformConfig['isInstalled']
            print(command)
            result = subprocess.run(command.split())
            return result.returncode is 0
        pass

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package {} is already installed".format(packageName))
            return
        logging.debug("{}: installing package {}".format(self.__class__.__name__, packageName))
        command = platformConfig['installCommand']
        if command:
            subprocess.run(command.split(), check=True)