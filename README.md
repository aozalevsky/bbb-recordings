# Description

This is a simple Flask-based app to serve full recordings list 
from BigBlueButton server, since Greenlight does not provide this 
functionality since v2.8.0.

The basic idea is to fetch recording list from the BBB server once
in a while and simply render the full list with as a web-page with 
the same basic features (search, sorting) as in Greenlight. 


# Installation

Install system dependencies:
```
sudo apt-get install git curl
```

Clone the repository with `git`:

```
git clone https://github.com/aozalevsky/bbb-recordings.git
```

Python dependencies can be installed with `pip`:

```
cd bbb-recordings
sudo pip3 install -r requirements.txt
```

Change the username and password in the `app.py`:
```
users = {
    "admin": generate_password_hash("SOMERANDOMPASSWORD"),
}
```

Construct a request using ApiMate link:
```
sudo bbb-conf  --secret  # to view ApiMate link
```

type `getRecordings` in the `Custom API calls` cell and check the link 
at the top of the page. It will look like:
```
https://hostname/bigbluebutton/api/getRecordings?checksum=XXXX
```

Open the link the browser, depending on the number 
of records this may take a while (about 1 minute fo 2000 records)

Check that app is working properly:
```
curl https://hostname/bigbluebutton/api/getRecordings?checksum=XXXX -o /tmp/recordings.xml
flask run
```

Setup a cron job to fetch recordings every hour:
```
sudo apt-get install cron crontab
sudo crontab -e

# Fetch recording every hour
1 * * * * curl https://hostname/bigbluebutton/api/getRecordings?checksum=XXXX -o /tmp/recordings.xml
```

And a systemd service to run the app:
```
sudo nano /etc/systemd/system/bbb-recordings.service
```
with a following content:
```
[Unit]
Description=Custom BBB records list
After=network.target

[Service]
User=generic
WorkingDirectory=/path/to/bbb-recordings
ExecStart=/usr/local/bin/flask run --port 5001
Restart=always

[Install]
WantedBy=multi-user.target
```

And start the service:
```
sudo systemctl daemon-reload
sudo systemctl start bbb-recordings
sudo systemctl enable bbb-recordings
```

Verify that service works:
```
sudo journalctl -u bbb-recordings
```

# Ackwnoledgments
The core architecture of the flask app is based on a nice [post](https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates) by Miguel Grinberg.

# Contacts
Arthur Zalevsky <aozalevsky@gmail.com>
