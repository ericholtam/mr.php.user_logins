#!/bin/bash

# user_logins controller
CTL="${BASEURL}index.php?/module/user_logins/"

# Get the scripts in the proper directories
"${CURL[@]}" "${CTL}get_script/user_logins.py" -o "${MUNKIPATH}preflight.d/user_logins.py"

# Check exit status of curl
if [ $? = 0 ]; then
	# Make executable
	chmod a+x "${MUNKIPATH}preflight.d/user_logins.py"

	# Set preference to include this file in the preflight check
	setreportpref "user_logins" "${CACHEPATH}user_logins.plist"

else
	echo "Failed to download all required components!"
	rm -f "${MUNKIPATH}preflight.d/user_logins.py"

	# Signal that we had an error
	ERR=1
fi


