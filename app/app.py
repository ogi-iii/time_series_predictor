import os
from flask import Flask, render_template

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

@app.route('/results')
def results():
    title = "results"

    # TODO: module func

    # TODO: lambda API collaboration
    #       1) upload csv & img to s3
    #       2) write urls in dynamoDB

    return render_template('results.html', title=title)

@app.route('/history')
def history():
    title = "history"

    # TODO: history table

    # TODO: lambda API collaboration
    #       1) read lines from dynamoDB

    return render_template('history.html', title=title)

if __name__ == "__main__":
    app.run(debug=True)