# Press Shift+F10 to execute it or run python3 main.py in terminal

import os
import pandas
import time
import random
import hashlib
import urllib3
import logging
from db import *
from example_data import *

from flask import Flask, render_template
app = Flask(__name__)


DEBUGGING = int(os.environ.get('DEBUGGING', 10)) == 10
logger = logging.getLogger()
logger.setLevel(int(DEBUGGING))
http = urllib3.PoolManager()

@app.route("/")
def run_python_challenge():
    regions = []
    countries = []
    hash_languages = []
    times = []

    headers = {
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
        'x-rapidapi-key': "93522eb112msh386fa4efca6e579p1a40a6jsn39e90108d05d"
    }

    try:
        r = http.request('GET', 'https://restcountries-v1.p.rapidapi.com/all', headers=headers)
        if r.status != 200:
            all = data_response
            regions.append(all['region'])
        else:
            for country in r:
                regions = country['region']
    except Exception as e:
        logger.debug(f'API present error service : {r.status}', e)
        return

    for region in regions:
        start_time = time.time()
        try:
            r = http.request('GET', 'https://restcountries-v1.p.rapidapi.com/region/%s' % region, headers=headers).content
            logger.debug(f'API present error service: {r.status}')
            country_seed = random.randint(0, len(r) - 1)
            countries.append(r[country_seed]['name'])
            hash_languages.append(hashlib.sha1(r[country_seed]['languages'][0]['name'].encode()).hexdigest())
        except Exception as e:
            logger.debug(f'API present error service : {r.status}', e)
            countries = all['name']
            country_seed = all['languages']
            sha1 = hashlib.sha1(str(country_seed).encode()).hexdigest()
            hash_languages = sha1
        end_time = time.time()
        times.append(end_time - start_time)

    df = pandas.DataFrame({
        "Region": regions,
        "City Name": countries,
        "Language": hash_languages,
        "Time [s]": times
    })
    df.to_json(path_or_buf='data.json')

    time_data = {'total': df['Time [s]'].sum().round(2), 'mean': df['Time [s]'].mean().round(2),
                 'min': df['Time [s]'].min().round(2), 'max': df['Time [s]'].max().round(2)}

    db = get_db()
    insert_db(db, countries, regions, time_data)
    db.commit()

    print("Table to json", df.to_json(orient='columns'))

    table_to_html = [df.to_html(index=False, justify='center', classes='table', )]

    return render_template('index.html', tables=table_to_html, statistics=time_data)


if __name__ == '__main__':
    app.run()
    run_python_challenge()
