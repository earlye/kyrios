
class packageManager:
    def isInstalled(self, packageName, package, context, platformConfig):
        '''
        Abstract method only. Child classes should implement this.
        '''
        raise NotImplementedError()

    def installPackage(self, packageName, package, context, platformConfig):
        '''
        Abstract method only. Child classes should implement this.
        '''
        raise NotImplementedError()

