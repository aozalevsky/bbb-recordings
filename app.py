# save this as app.py
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import xmltodict
import time
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("SOMERANDOMPASSWORD"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route("/")
@auth.login_required
def index():
    with open('/tmp/recordings.xml', 'r') as f:
        raw = f.readlines()

    data = xmltodict.parse(''.join([x.strip() for x in raw]))
    if data['response']['returncode'] == 'SUCCESS':
        rawrecords = data['response']['recordings']['recording']

        records = list()

        for r in rawrecords:
            name = r['name']
            ts = int(r['startTime'][:-3])
            date = datetime.fromtimestamp(ts).strftime('%d.%m.%Y')
            stime = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            duration_raw = int(r['playback']['format']['length'])
            duration = time.strftime("%H:%M:%S", time.gmtime(duration_raw * 60))
            url = r['playback']['format']['url']
            previews = r['playback']['format']['preview']['images']['image']
            if type(previews) is list:
                preview = previews[0]['#text']
            elif type(previews) is OrderedDict:
                preview = previews['#text']
            else:
                print(r)
                continue

            d = {
                'name': name,
                'timestamp': ts,
                'date': date,
                'time': stime,
                'duration_raw': duration_raw,
                'duration': duration,
                'url': url,
                'preview': preview,
            }

            records.append(d)

        records = sorted(records, key=lambda x: x['timestamp'], reverse=True)

        return render_template("bootstrap_table.html", title='Recording list',
                        records=records)

if __name__ == '__main__':
    app.run()
