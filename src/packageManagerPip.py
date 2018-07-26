
from packageManager import packageManager
import logging
import stdplus

class packageManagerPip(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        managedPackageName = platformConfig['packageName']
        command = "pip show '{}' > /dev/null".format(managedPackageName)
        result = stdplus.run(command, throwOnNonZero = False)
        return result is 0

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package '{}' is already installed".format(packageName))
            return
        logging.debug("{}: installing package '{}'".format(self.__class__.__name__, packageName))
        managedPackageName = platformConfig['packageName']
        command = "pip install '{}'".format(managedPackageName)
        stdplus.run(command)

