#!/usr/local/bin/python3
"""
Name: Screen Shot Cleanup
Author: Kyle Fennell
OS: MacOS running python3
Description: This script will install a daemon that will remove any screen shots
    from the desktop that haven't been accessed in 30 days or more. Moving
    the script after it's been run will break the daemon.

    This script can also be run on it's own to remove screen shot files, but
    ensure the plist is not in the current path.

Target file example: "Screen Shot 2020-09-30 at 9.48.25 PM.png"
"""
import logging
import os
import re
import time


USER = os.getlogin()
HOME_PATH = '/Users/{}'.format(USER)
PLIST = 'local.screen_shot_cleanup.plist'
SCRIPT_PATH = os.path.join(os.getcwd(), 'screen_shot_cleanup.py')
LOG_PATH = '{}/Library/Logs/Screen Shot Cleanup.log'.format(HOME_PATH)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename=LOG_PATH, level='INFO')


def setup():
    """Setup the daemon. Add the script path the the plist file, move it
        to the correct location and load the daemon.
    """
    logging.info('Attempting to setup daemon.')
    try:
        with open(PLIST, 'r') as plist_file:
            new_file = []
            for line in plist_file.readlines():
                if '<string>path_to_script</string>' in line:
                    new_file.append('  <string>{}</string>\n'.format(SCRIPT_PATH))
                else:
                    new_file.append(line)
        with open(PLIST, 'w') as plist_file:
            for line in new_file:
                plist_file.write(line)
        os.rename(PLIST, '{}/Library/LaunchAgents/{}'.format(HOME_PATH, PLIST))
        os.system('launchctl load {}/Library/LaunchAgents/{}'.format(HOME_PATH, PLIST))
        logging.info('Daemon setup complete.')
    except Exception as error:
        logging.error('setup(): %s', error)


def main():
    """The daemon calls this function everyday at 10am. If the plist file is
        still in the current path, then we run setup() to load the daemon,
        otherwise we proceed to check the desktop for any screen shots that have
        not been accessed in 30 days or more, and remove them.
    """
    if os.path.isfile(PLIST):
        setup()
    path = "{}/Desktop".format(HOME_PATH)
    try:
        with os.scandir(path) as directory:
            for entry in directory:
                screen_shot = re.search('^Screen Shot \d\d\d\d-\d\d-\d\d at .+png$', entry.name)
                screen_shot_time = os.stat(entry.path).st_atime
                is_gt_30days = screen_shot_time <= (time.time() - 2592000)
                if screen_shot and is_gt_30days:
                    os.remove(entry.path)
                    logging.info('Removed %s', entry.name)
    except Exception as error:
        logging.error('main(): %s', error)


main()
