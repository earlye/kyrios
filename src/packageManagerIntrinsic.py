from packageManager import packageManager
import logging

class packageManagerIntrinsic(packageManager):
    def isInstalled(self, packageName, package, context, platformConfig):
        return True

    def installPackage(self, packageName, package, context, platformConfig):
        pass # it's intrinsically there!
