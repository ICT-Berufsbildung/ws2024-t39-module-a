#!/bin/bash

# Check grading scripts are 
if [ ! -d /usr/local/share/grading ]; then
    echo "Please enter the passphrase to decrypt the marking scripts"
    if ! unzip -qq /usr/local/share/wsc_grading.zip -d /usr/local/share; then
        rm -rf /usr/local/share/grading/
    fi
fi
# Run grading script
/usr/local/share/grading/grading.py "$@"
