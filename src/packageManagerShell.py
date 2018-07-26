
from packageManager import packageManager
import logging
import stdplus

class packageManagerShell(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        if 'isInstalled' in platformConfig:
            command = platformConfig['isInstalled']
            result = stdplus.run(command, throwOnNonZero = False)
            return result is 0
        pass

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package '{}' is already installed".format(packageName))
            return
        logging.debug("{}: installing package '{}'".format(self.__class__.__name__, packageName))
        command = platformConfig['installCommand']
        if command:
            stdplus.run(command)

