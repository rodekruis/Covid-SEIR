import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import locale
import matplotlib.patches as mpatches
from src.io_func import load_config
country = 'OPT'
save_dirs = ['output/OPT/final-plots']
configpath = 'configs/OPT.json'

config = load_config(configpath)
pop = config['population']
sigma = config['sigma']

locale.setlocale(locale.LC_ALL, "nl_NL")
today = datetime.today().strftime("%d-%B-%Y").lower()
span = datetime.today() - datetime.strptime('1-maart-2020', "%d-%B-%Y")
short = span.days + 7
long = span.days + 100

labels = ['S', 'E', 'REM', 'I', 'REC', 'HOS', 'D']
dfs = []
for label in labels:
    data_phl = pd.read_csv('output/{}/{}_{}_prob.csv'.format(country, country, label),
                          header=None,
                          names=['time', label, label+'5', label+'30', label+'50', label+'70', label+'95'],
                          index_col=False)
    data_phl = data_phl[1:]
    dfs.append(data_phl)
data_h = pd.concat(dfs, axis=1)
data_h = data_h.loc[:, ~data_h.columns.duplicated()]

time_span = len(data_h)
time = pd.date_range(start='3/1/2020', periods=time_span)
df = data_h.astype(float)

# keep only last 90 days
df = df[-90:]
time = time[-90:]
print(time[-1])

# compute variables to show
# NI new cases
# ND new deaths
# ICUM cumulative cases
for suff in ['', '5', '30', '50', '70', '95']:
    df['NI'+suff] = df['E'+suff] * sigma
df['ND'] = df['D'].diff()
for suff in ['5', '30', '50', '70', '95']:
    df['ND' + suff] = (df['D' + suff] - df['D']) * 0.05 + df['ND']
for suff in ['', '5', '30', '50', '70', '95']:
    df['ICUM'+suff] = pop - df['S'+suff]

# drop first row because it's NaN after differentiating
df = df[1:]
time = time[1:]

labels = ['NI', 'ND', 'ICUM', 'D']
labels_verbose = ["new cases", "new deaths", "total cases", "total deaths"]

for lab, labv in zip(labels, labels_verbose):
    plt.figure()
    if 'CUM' in lab:
        max = df[lab].to_numpy().max() * 1.15
        min = df[lab].to_numpy().min() * 0.85
    else:
        max = df[lab].to_numpy().max() * 1.5
        min = 1
    print(lab, min, max)
    datal = df[lab].to_numpy()
    plt.plot(time, datal, label=labv)
    plt.fill_between(time, df[lab+'30'], df[lab+'70'], alpha=0.1, label=None)
    plt.xlabel("date")
    plt.title("COVID-19 {} forecasts".format(country))
    plt.ylabel(labv)
    # plt.axvline(datetime.strptime('13-03-2020', '%d-%m-%Y'), 0, max, label='measures introduced', linestyle='--',
    #             color='black')
    plt.axvline(datetime.today(), 0, max, label='today', linestyle='-', color='black')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.ylim([min, max])
    # plt.semilogy()

    handles, labels = plt.gca().get_legend_handles_labels()
    blue_patch = mpatches.Patch(color='blue', alpha=0.1, label='70% CI')
    handles.append(blue_patch)
    plt.legend(handles=handles)

    for save_dir in save_dirs:
        if not os.path.exists(save_dir + '/' + today):
            os.mkdir(save_dir + '/' + today)
        plt.savefig(save_dir + '/' + today +'/forecast_'+country+'_'+labv+'.png')
        print(save_dir + '/' + today +'/forecast_'+country+'_'+labv+'.png')
    # plt.show()
