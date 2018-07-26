# Package YAML Syntax

* description: String, hopefully self-evident
* webPage: String, The maintainers' website for this package manager
* platforms: Dictionary
  * _platform-name_: Dictionary (use `platform.system()` in python to get this name.) Isn't just "platform-name" literally.
    * dependencies: Array of Strings, packages required for successful installation; each must exist in another package YAML file
    * isInstalled: String, commandline invocation that will return 0 if and only if this package is already installed
    * options: String, commandline arguments for homebrew; only use with homebrew. 
    * packageManager: String, which packageManager is used to install this package (homebrew, npm, pip or shell currently) 
    * packageName: String, the identifier for this package to be used by other package YAML files
    * postInstall: String, commandline invocation to run after installation completes
    * exitKyrios: Boolean,  Whether you must exit Kyrios in order to finish the installation of this package. 
