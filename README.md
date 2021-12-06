# LED Pi project
Client script that calls a REST API I developed for my Pi-hole. 
The client script also interacts with the Raspberry Pi's GPIO to drive two LEDs and a button. 
The button is used to enable/disable blocking YouTube with Pi-hole.
The LEDs indicate the blocked/unblocked state of YouTube.


# From Python Console
`PI_PASSWD=<password> python3 `


# Systemd Service
Hand the password to the service.

sudo systemctl start yt-block@<password>.service