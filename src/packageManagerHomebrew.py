
from packageManager import packageManager
import logging
import stdplus

class packageManagerHomebrew(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        managedPackageName = platformConfig['packageName']
        options = platformConfig.get('options', '')
        command = "brew {} ls --versions '{}' > /dev/null".format(options, managedPackageName)
        result = stdplus.run(command, throwOnNonZero = False)
        return result is 0

    def installPackage(self, packageName, package, context, platformConfig):
        if self.isInstalled(packageName, package, context, platformConfig):
            logging.debug("package '{}' is already installed".format(packageName))
            return
        logging.debug("{}: installing package '{}'".format(self.__class__.__name__, packageName))
        managedPackageName = platformConfig['packageName']
        options = platformConfig.get('options', '')
        command = "brew {} install '{}'".format(options, managedPackageName)
        stdplus.run(command)
        postInstall = platformConfig.get('postInstall', False)
        if postInstall:
            stdplus.run(postInstall)
        if platformConfig.get('exitKyrios', False):
            logging.debug("Package '{}' is installed, but the act of doing that requires running kyrios again. Sorry!".format(packageName))
            exit(0)

