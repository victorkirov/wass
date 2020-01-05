# wass
Web Accessible Slideshow Server

Requires:
- Python 3.7+ (e.g. sudo apt install python3.8)
- Python 3.7+ venv (e.g. sudo apt install python3.8-venv)
- tkinter (e.g. sudo apt install python3.8-tk)

## Install
TODO

## Available ENV variables
TODO

## Run from terminal
TODO

## Run in supervisor
Ensure supervisor is installed by running `sudo apt install -y supervisor`

Edit `./etc/supervisor/wass.conf` and enter the directory to the wass project under the `command` and `directory` entries. Also, if you are not using the default `pi` user, update the `user` entry to the correct user. Finally, edit the environment variables under the `environment` entry to match the correct ones for your system as per the available variables above.

Run the below command to configure the app with supervisor (I'm using the project directory `/home/pi/Projects/wass`. change the directory to the correct one on your system):
`sudo ln -s /home/pi/Projects/wass/etc/supervisor/wass.conf /etc/supervisor/conf.d`

Update supervisor by executing `sudo supervisorctl` followed by `update`.

## Access the API
TODO

## Disable screen sleep on Raspbian
Note: For all commands below, add `DISPLAY=:0` at the beginning if running via ssh

To check settings execute `xset q` in terminal

To disable screensaver, set timeout to zero `xset s 0`

To disable EnergyStar, run `xset -dpms`

For example, if running from ssh, the following commands will print the current settings, disable the screensaver, disable EnergyStar, and print the final settings:
```
DISPLAY=:0 xset q
DISPLAY=:0 xset s 0
DISPLAY=:0 xset -dpms
DISPLAY=:0 xset q
```

To survive a reboot, add these lines to the bottom of your `~/.profile` file:
```
DISPLAY=:0 xset s 0
DISPLAY=:0 xset -dpms
```

## Instructions to sync Google Drive in Linux
https://github.com/pageauc/rclone4pi/wiki
