#!/usr/local/munkireport/munkireport-python3
"""
Parse user sessions on macOS so we can determine what users logged in and
when the event took place. We only obtain 'console' and 'ssh' sessions as
regular 'ttys' sessions are less useful as a whole.

Original Author: Clayton Burlison - https://clburlison.com
Adapatations for User Logins: Eric Holtam - https://osxbytes.wordpress.com, @eholtam on Slack & Twitter

Code from: Michael Lynn -
    https://gist.github.com/pudquick/7fa89716fe2a8f6cdc084958671b7b58

Created for MunkiReport - https://github.com/munkireport/munkireport-php
"""

from ctypes import (CDLL,
                    Structure,
                    POINTER,
                    c_int64,
                    c_int32,
                    c_int16,
                    c_char,
                    c_uint32)
from ctypes.util import find_library
import plistlib
import os
import sys
import time

# constants
c = CDLL(find_library("System"))
BOOT_TIME = 2
USER_PROCESS = 7
DEAD_PROCESS = 8
SHUTDOWN_TIME = 11


class timeval(Structure):
    _fields_ = [
                ("tv_sec",  c_int64),
                ("tv_usec", c_int32),
               ]


class utmpx(Structure):
    _fields_ = [
                ("ut_user", c_char*256),
                ("ut_id",   c_char*4),
                ("ut_line", c_char*32),
                ("ut_pid",  c_int32),
                ("ut_type", c_int16),
                ("ut_tv",   timeval),
                ("ut_host", c_char*256),
                ("ut_pad",  c_uint32*16),
               ]


def fast_last(session='gui_ssh'):
    """This method will replicate the functionallity of the /usr/bin/last
    command to output all logins, reboots, and shutdowns. We then calculate
    the logout.

    session takes on of the following strings:
        * gui
        * gui_ssh
        * all
    """
    # local constants
    setutxent_wtmp = c.setutxent_wtmp
    setutxent_wtmp.restype = None
    getutxent_wtmp = c.getutxent_wtmp
    getutxent_wtmp.restype = POINTER(utmpx)
    endutxent_wtmp = c.setutxent_wtmp
    endutxent_wtmp.restype = None
    # data storage
    events = []
    # initialize
    setutxent_wtmp(0)
    entry = getutxent_wtmp()
    while entry:
        e = entry.contents
        entry = getutxent_wtmp()
        event = {}
        if (e.ut_type == USER_PROCESS) or (e.ut_type == DEAD_PROCESS):
            # filter out system account _mdsetupuser
            if (e.ut_user == "_mbsetupuser" or e.ut_user == "root"):
                continue
            else:
                event = {'user': e.ut_user}
        if event != {}:
            events.append(event)
    # finish
    endutxent_wtmp()
    user_logins =  list({v['user']:v for v in events}.values())
    return user_logins
    
def main():
    """Main"""
    # Create cache dir if it does not exist
    cachedir = '%s/cache' % os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # Skip manual check
    if len(sys.argv) > 1:
        if sys.argv[1] == 'manualcheck':
            print('Manual check: skipping')
            exit(0)

    # Get results
    result = fast_last()

    # Write user session results to cache
    output_plist = os.path.join(cachedir, 'user_logins.plist')
    try:
        plistlib.writePlist(result, output_plist)
    except:
        with open(output_plist, 'wb') as fp:
            plistlib.dump(result, fp, fmt=plistlib.FMT_XML)


if __name__ == "__main__":
    main()
