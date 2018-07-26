# Package YAML Syntax

* description: String, hopefully self-evident
* webPage: String, The maintainers' website for this package manager
* platforms: Dictionary
  * platform-name: Dictionary (use `platform.system()` in python to get this name.) Isn't just "platform-name" literally.
    * dependencies: Array of Strings, packages required for successful installation; each must exist in another package YAML file
    * isInstalled: String, command line invocation that will return 0 if and only if this package is already installed
    * packageManager: String, which packageManager is used to install this package (homebrew, npm, pip or shell currently) 
    * packageName: String, the identifier for this package to be used by other package YAML files

