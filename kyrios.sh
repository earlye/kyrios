#!/bin/bash
#
# This script provisions a host.
#

function gte() {
    [[ "$1" == "$2" || "$1" > "$2" ]]
}


# python3 ships with macOS Catalina
PYTHON=$(which python3 || which python)
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
    elif (gte "${python_version}" "Python 3.7"); then
        echo "DEBUG: which python?:${PYTHON}"
        echo "DEBUG: python version:${python_version}"
    fi
fi

${PYTHON} src/setup.py --quiet install --user
${PYTHON} src/kyrios.py $*
