#!/bin/bash

# Remove user_logins script
rm -f "${MUNKIPATH}preflight.d/user_logins.py"

# Remove user_logins.plist file
rm -f "${CACHEPATH}user_logins.plist"
