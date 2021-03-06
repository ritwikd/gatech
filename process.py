from datetime import timedelta
from flask import Flask,make_response, request, current_app
from functools import update_wrapper
import requests, nltk, shlex
import pymongo

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
app = Flask(__name__)



@app.route('/moves=<access_token>')
@crossdomain(origin='*')
def getMoves(access_token):
    authH = {
        'Authorization' : 'Bearer ' + access_token
    }
    print access_token
    x = access_token
    requestData = requests.get('https://jawbone.com/nudge/api/v.1.1/users/@me/moves', headers=authH);
    return requestData.text

@app.route("/weather=<airport>")
@crossdomain(origin='*')
def getWeah(airport):
    requestData = requests.get("http://aviationweather.gov/adds/metars/?station_ids=" + airport + "&std_trans=standard&chk_metars=on&hoursStr=past+24+hours&submitmet=Submit");
    weatherData = nltk.clean_html(requestData.text)
    weatherData = weatherData.split(" ")
    temps = []
    for term in weatherData:
        if (len(term) == 5 and '/' in term):
            temps.append(term.split("/")[0])

    return x

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
