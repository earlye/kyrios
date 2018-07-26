#!/bin/bash
#
# This script provisions a host.
#

function gte() {
    [[ "$1" == "$2" || "$1" > "$2" ]]
}


# Make sure python 2.7 is installed
# We go w/ 2.7 because that's what's preinstalled on macOS, not because it's a particularly
# good choice.
PYTHON=$(which python2 || which python)
if [[ "${PYTHON}" == "" ]]; then
    echo "Python is not installed. Install python before provisioning."
    exit
else
    python_version=$(${PYTHON} --version 2>&1)
    if [[ "${python_version}" < "Python 2.7" ]]; then
        echo "DEBUG: which python?:${PYTHON}"
        echo "DEBUG: python version:${python_version}"
        echo "ERROR: Upgrade ${python_version} to 2.7 before provisioning."
        exit
    elif (gte "${python_version}" "Python 2.8"); then
        echo "DEBUG: which python?:${PYTHON}"
        echo "DEBUG: python version:${python_version}"
        echo "WARN: ${python_version} >= 2.8. Untested python version"
    fi
fi

# Make sure pip is installed
PIP=$(which pip2 || which pip)
if [[ "${PIP}" == "" ]]; then
    echo "PIP is not installed. Install pip before provisioning."
    echo "try: sudo easy_install pip"
    exit
fi

${PIP} install stdplus
${PYTHON} src/kyrios.py $*
