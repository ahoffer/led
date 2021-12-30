# LED Pi project

Client script that calls a REST API I developed for my Pi-hole. The client script also interacts with the Raspberry Pi's
GPIO to drive two LEDs and a button. The button is used to enable/disable blocking YouTube with Pi-hole. The LEDs
indicate the blocked/unblocked state of YouTube.

# From Python Console

`PI_PASSWD=<password> python3`

# Systemd Service

1. Create the service file
   `/etc/systemd/system/yt-block.service`

2. Create override conf file for the pihole password `systemctl edit yt-block`

3. Add the environment variable with password

```
[Service]
Environment=PI_PASSWD=<password>
```

4. Start and enable the service

```
systemctl daemon-reload
systemctl start yt-block.service
systemctl enable yt-block.service

```

To see what is happening

`journalctl -u yt-block`

## Packaging


#### Upload to PyPi Test

    python3 -m twine upload --repository testpypi dist/*

    Username: __token__
    Password: API token


#### Install from PyPi Test

    python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ youtubeblocker
