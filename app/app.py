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
from module import *


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
    title = "index"
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

    # TODO: lambda API collaboration
    # 1) upload csv & img to s3
    # 2) write urls in dynamoDB
    # url = "http://xxxx/xxxx"
    # json_data = json.dumps({
    #     "img": img_base64,
    #     "df_dict": output_df.to_dict(),
    #     "df_index": index_col,
    #     }).encode("utf-8")
    # method = "POST"
    # headers = {"Content-Type" : "application/json"}
    # request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    # with urllib.request.urlopen(request) as response:
    #     response_body = response.read().decode("utf-8")
    #     result_objs = json.loads(response_body)
    # df = pd.DataFrame().from_dict(results_dict["df_dict"])
    # df.index.name = results_dict["df_index"]

    return render_template('results.html', title=title, img_base64=img_base64)


@app.route('/history')
def history():
    title = "history"

    # TODO: lambda API collaboration
    #       1) read lines from dynamoDB

    # あとで消す
    history = []
    history.append({
        "date": "2020-09-28 00:17:31.716364",
        "name": "AirPassengers",
        "plot": "https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv",
        "csv": "https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv",
        })
    history.append({
        "date": "2020-09-29 10:17:31.716364",
        "name": "AirPassengers2",
        "plot": "https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv",
        "csv": "https://www.analyticsvidhya.com/wp-content/uploads/2016/02/AirPassengers.csv",
        })
    # ここまで

    return render_template('history.html', title=title, enumerate_hist=enumerate(history))


if __name__ == "__main__":
    app.run(debug=True)