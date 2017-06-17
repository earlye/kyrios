#!/bin/bash -e
#
# This script provisions a host.
#

# Make sure python is installed
echo "DEBUG: Checking python version"
python_version=$(python2 --version 2>&1)
echo "DEBUG: python version:${python_version}"
if [[ "${python_version}" < "Python 2.7" ]]; then
    echo "ERROR: Upgrade ${python_version} to 2.7 before provisioning."
    exit
fi

if [[ "${python_version}" > "Python 2.8" || "${python_version}" == "Python 2.8" ]]; then
    echo "WARN: ${python_version} >= 2.8. Untested python version"
fi

# Make sure pip is installed
echo "DEBUG: Checking pip version"
pip_version=$(pip2 --version 2>&1)
echo "DEBUG: pip_version:${pip_version}"
if [[ "${pip_version}" < "pip 9.0" ]]; then
    echo "ERROR: Upgrade '${pip_version}' to 9.0 before provisioning."
    exit
fi

pip install stdplus
python2 kyrios.py $*
