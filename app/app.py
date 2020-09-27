import os
import base64
import numpy as np
import pandas as pd
from scipy import stats
from scipy import signal
import statsmodels.api as sm
from matplotlib import pyplot as plt
import seaborn as sns
sns.set() #plotの準備
import warnings
warnings.filterwarnings('ignore') # 計算警告を非表示

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
    # requestから受け取る
    file = request.files['csvFile']
    csv_name = file.filename
    index_col = request.form["datetimeIndex"]
    target_col = request.form["targetColumn"]
    pred_begin = str(request.form["predBeginDate"]).replace('/', '-') + " " + str(request.form["predBeginTime"])
    pred_end = str(request.form["predEndDate"]).replace('/', '-') + " " + str(request.form["predEndTime"])
    # SARIMA実行
    with tempfile.NamedTemporaryFile() as tf:
        csv = tf.name
        file.save(csv)
        ts = read_data(csv,
                    index_col,
                    target_col
                    )
    p, d, q, sfq = select_order(ts, d = 1, freq_order = 5)
    sarimax = fit_sarima(ts, p, d, q, sfq, sp = 1, sd = 1, sq = 1)
    # csvと画像の出力
    with tempfile.TemporaryDirectory() as temp_dir:
        plot_fname, csv_fname = output_results(sarimax,
                                            pred_begin,
                                            pred_end,
                                            ts,
                                            csv_name,
                                            index_col,
                                            target_col,
                                            temp_dir,
                                            temp_dir,
                                            )
        with open(os.path.join(temp_dir, plot_fname), "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')

        # TODO: csvファイルのdict化

    # TODO: lambda API collaboration
    #       1) upload csv & img to s3
    #       2) write urls in dynamoDB

    return render_template('results.html', title=title, img_base64=img_base64)


@app.route('/history')
def history():
    title = "history"

    # TODO: history table

    # TODO: lambda API collaboration
    #       1) read lines from dynamoDB

    return render_template('history.html', title=title)


if __name__ == "__main__":
    app.run(debug=True)