import os
import base64
import json
import urllib
import numpy as np
import pandas as pd
from scipy import stats
from scipy import signal
import statsmodels.api as sm
from matplotlib import pyplot as plt
import seaborn as sns
sns.set() #plot preparation
import warnings
warnings.filterwarnings('ignore') # ignore warning

from flask import Flask, render_template, request
import tempfile
from module.sarima import *


app = Flask(__name__)


@app.context_processor # clear web cash
def add_staticfile():
    def staticfile_cp(fname):
        path = os.path.join(app.root_path, 'static', fname)
        mtime =  str(int(os.stat(path).st_mtime))
        return '/static/' + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)


@app.route('/')
def index():
    title = ""
    return render_template('index.html', title=title)


@app.route('/analysis')
def analysis():
    title = "analysis"
    return render_template('analysis.html', title=title)


@app.route('/results', methods=['POST'])
def results():
    title = "results"
    # form comtents
    file = request.files['csvFile']
    csv_name = file.filename
    index_col = request.form["datetimeIndex"]
    target_col = request.form["targetColumn"]
    pred_begin = str(request.form["predBeginDate"]).replace('/', '-') + " " + str(request.form["predBeginTime"])
    pred_end = str(request.form["predEndDate"]).replace('/', '-') + " " + str(request.form["predEndTime"])
    # learning process
    with tempfile.NamedTemporaryFile() as tf:
        csv = tf.name
        file.save(csv)
        ts = read_data(csv,
                    index_col,
                    target_col
                    )
    p, d, q, sfq = select_order(ts, d = 1, freq_order = 5)
    sarimax = fit_sarima(ts, p, d, q, sfq, sp = 1, sd = 1, sq = 1)
    # output csv & image
    with tempfile.TemporaryDirectory() as temp_dir:
        plot_fname, output_df = output_results(sarimax,
                                            pred_begin,
                                            pred_end,
                                            ts,
                                            csv_name,
                                            index_col,
                                            target_col,
                                            temp_dir,
                                            )
        with open(os.path.join(temp_dir, plot_fname), "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        fname = "tmp.csv"
        output_df.to_csv(os.path.join(temp_dir, fname))
        with open(os.path.join(temp_dir, fname)) as f:
            csv_str = f.read()

    # TODO: API URL Auto Reference #
    url = "https://5zl66imvp6.execute-api.ap-northeast-1.amazonaws.com/Prod/createFiles"
    # until this line #

    json_data = json.dumps({
        "fname": csv_name,
        "img_base64": img_base64,
        "csv_str": csv_str,
        }).encode("utf-8")
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    api_request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(api_request) as response:
        response_body = response.read().decode("utf-8")
        result_obj = json.loads(response_body)
        img_url = result_obj["img_url"]
        csv_url = result_obj["csv_url"]

    return render_template('results.html', title=title, img_base64=img_base64, img_url=img_url, csv_url=csv_url)


@app.route('/history')
def history():
    title = "history"

    # TODO: API URL Auto Reference #
    url = "https://lecpabuvjd.execute-api.ap-northeast-1.amazonaws.com/Prod/history"
    # until this line #

    api_request = urllib.request.Request(url)
    with urllib.request.urlopen(api_request) as response:
        response_body = response.read().decode("utf-8")
        history_obj = json.loads(response_body)

    history = []
    for key, hist in history_obj.items():
        history.append({
            "id": key,
            "timestamp": hist["timestamp"],
            "name": hist["name"],
            "img_url": hist["img_url"],
            "csv_url": hist["csv_url"],
            })

    return render_template('history.html', title=title, history=history)


if __name__ == "__main__":
    app.run(debug=True)