import os
import datetime
import numpy as np
import pandas as pd
from scipy import stats
from scipy import signal
import statsmodels.api as sm
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

def read_data(csv: str,
            index_col: str,
            target_col: str
            ) -> pd.Series:
    return pd.read_csv(csv, index_col=index_col, parse_dates=True, dtype=float)[target_col]


def _fill_missing(ts: pd.Series,
            method: str = 'cubic'
            ) -> pd.Series:
    return ts.interpolate(method=method, limit_direction='forward', limit_area='inside')


def _estimate_freq(ts_diff: pd.Series,
                freq_order: int = 5,
                missing: str = False
                ) -> int:
    if missing:
        freq = sm.tsa.stattools.acf(ts_diff)
    else:
        fft = np.fft.fft(ts_diff)
        freq = np.abs(fft)
    return int(signal.argrelmax(freq, order=freq_order)[0][0]) # frequency


def _select_order(ts: pd.Series,
                d: int = 1,
                freq_order: int = 5,
                missing: str = False
                ) -> list:
    if missing:
        ts = _fill_missing(ts, method='cubic')
    ts_diff = ts.diff(d).dropna() # difference time-series
    aosi = sm.tsa.arma_order_select_ic(ts_diff, ic='aic', trend='nc')
    p, q = aosi['aic_min_order']
    sfq = _estimate_freq(ts_diff, freq_order, missing)
    return [p, d, q, sfq]


def fit_sarima(ts: pd.Series,
            sp: int = 1,
            sd: int = 1,
            sq: int = 1,
            missing: str = False
            ):
    p, d, q, sfq = _select_order(ts,
                d = 1,
                freq_order = 5,
                missing = missing
                )
    sarimax = sm.tsa.SARIMAX(ts,
                            order=(p, d, q),
                            seasonal_order=(sp, sd, sq, sfq),
                            enforce_stationarity = False,
                            enforce_invertibility = False
                            ).fit()
    return sarimax


def output_results(sarimax,
                pred_begin: str,
                pred_end: str,
                ts: pd.Series,
                csv_name: str,
                index_col: str,
                target_col: str,
                output_fig_dir: str,
                missing: str = False
                ) -> list:
    dt_now = datetime.datetime.now()
    ts_pred = sarimax.get_prediction(pred_begin, pred_end)
    pred_conf_int = ts_pred.conf_int(alpha=0.05) # 95%

    plot_fname = f"{dt_now}_{csv_name.split('/')[-1].split('.')[0]}.png"

    # predict future values
    fig = plt.figure(figsize=(12, 5))
    plt.title(csv_name.split('/')[-1].split('.')[0], fontsize=15)
    if missing:
        ts_filled = _fill_missing(ts, method='cubic')
        plt.plot(ts_filled, "g", label="filled")
    plt.plot(ts, label="original")
    plt.plot(ts_pred.predicted_mean, "--r", label="prediction")
    plt.fill_between(pred_conf_int.index, pred_conf_int.iloc[:, 0], pred_conf_int.iloc[:, 1],
                    color='orange', alpha=0.4, label="95% confidence interval")
    plt.ylabel(target_col)
    plt.xlabel(index_col)
    plt.xticks(rotation=45)
    plt.legend()
    fig.savefig(os.path.join(output_fig_dir, plot_fname), bbox_inches="tight")
    plt.close(fig)

    # summarise prediction results to csv
    output_df = pd.concat([ts, ts_pred.predicted_mean, pred_conf_int], axis=1)
    output_df.columns = [output_df.columns[0], f"prediction {output_df.columns[0]}",
                        pred_conf_int.columns[0], pred_conf_int.columns[1]]
    output_df.index.name = index_col

    return [plot_fname, output_df]
