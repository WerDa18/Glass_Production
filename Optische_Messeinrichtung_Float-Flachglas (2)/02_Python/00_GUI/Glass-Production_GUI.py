from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
from PIL import Image, ImageTk
from time import localtime
import pandas as pd
import numpy as np
import matplotlib
import decimal
import datetime
import math
import boto3
matplotlib.use("TkAgg")

# SETTINGS_____________________________________________________________________________________________________________
progress = 0
max_bytes = 50000

after_id = None
inner_radius = 6
distance_center = 62
band_width = 57
paper_thickness = 0.154

p = {'production_time_h': 1, 'production_start': 0, 'n': 60, 'counter': 0, 'last_update': 0}

spec = {'high': 150, 'medium': 100, 'low': 50, 'iO': 20}
vs = {'ldr_grau': 511, 'ldr_weiss': 511, 'ldr_blau': 511, 'ldr_gelb': 360, 'ldr_lila': 511, 'ldr_gruen': 511}

d = {'x_values_min_mat': [0], 'x_values_min_speed': [0], 'x_values_min_stock': [0], 'y_mat': [0], 'y_speed': [0], 'rotation_cache': [], 'y_stock': [0], 'ms': [0], 'col': ['white'],
     'update_time': 60000, 'dot_size_high': 200, 'dot_size_medium': 100, 'dot_size_low': 2, 'limit_medium': 150, 'limit_low': 100}

k = {'high_def_lbl': 0, 'medium_def_lbl': 0, 'low_def_lbl': 0, 'total_def_lbl': 0, 'high_def_mm': 15, 'medium_def_mm': 10, 'low_def_mm': 5, 'performance': 1, 'availability': 1, 'quality': 1, 'oee': 1}


# WINDOW AND BACKGROUND SETTINGS ______________________________________________________________________________________
window = Tk()
window.resizable(0, 0)
window.title("IoT Monitoring: Glass Production Model")

bg_png = ImageTk.PhotoImage(Image.open("src/bg.png"))
bg_lbl = Label(window, bg='black', image=bg_png)
bg_lbl.pack()

y_cor = int((window.winfo_screenheight()-bg_lbl.winfo_reqheight())/2)
x_cor = int((window.winfo_screenwidth()-bg_lbl.winfo_reqwidth())/2)
window.geometry("+{}+{}".format(x_cor, y_cor-40))


# BUTTON ______________________________________________________________________________________________________________
start_cmd = Button(window, bg='spring green', text='start', height=2, width=8)
start_cmd.place(x=15, y=797)

stop_cmd = Button(window, bg='gray95', text='stop', height=2, width=8)
stop_cmd.place(x=92, y=797)


# KEY FIGURES LABEL ___________________________________________________________________________________________________
mm_def_lbl = Label(window, text='0',  font=('Arial', 12), bg='cyan4', fg='white')
mm_def_lbl.place(x=1120, y=187, anchor='e')

high_def_lbl = Label(window, text='0', font=('Arial', 12), bg='cyan4', fg='white')
high_def_lbl.place(x=1120, y=225, anchor='e')

medium_def_lbl = Label(window, text='0', font=('Arial', 12), bg='cyan4', fg='white')
medium_def_lbl.place(x=1120, y=263, anchor='e')

low_def_lbl = Label(window, text='0', font=('Arial', 12), bg='cyan4', fg='white')
low_def_lbl.place(x=1120, y=299, anchor='e')

total_def_lbl = Label(window, text='0', font=('Arial', 12), bg='cyan4', fg='white')
total_def_lbl.place(x=1120, y=337, anchor='e')

speed_lbl = Label(window, text='0', font=('Arial', 12), bg='cyan4', fg='white')
speed_lbl.place(x=1075, y=375, anchor='e')

performance_lbl = Label(window, text='0', font=('Arial', 10), bg='gray40', fg='white')
performance_lbl.place(x=1095, y=539, anchor='e')

availability_lbl = Label(window, text='0', font=('Arial', 10), bg='gray40', fg='white')
availability_lbl.place(x=1095, y=576, anchor='e')

quality_lbl = Label(window, text='0', font=('Arial', 10), bg='gray40', fg='white')
quality_lbl.place(x=1095, y=614, anchor='e')

oee_lbl = Label(window, text='0', font=('Arial', 10), bg='gray40', fg='white')
oee_lbl.place(x=1095, y=659, anchor='e')

prod_start_lbl = Label(window, font=('Arial', 10), bg='gray40', fg='white')
prod_start_lbl.place(x=305, y=755)

prod_laufzeit_lbl = Label(window, font=('Arial', 10), bg='gray40', fg='white')
prod_laufzeit_lbl.place(x=342, y=800, anchor='e')

prod_ende_lbl = Label(window, font=('Arial', 10), bg='gray40', fg='white')
prod_ende_lbl.place(x=305, y=822)


# CANVAS / FIGURES / SUBPLOTS / PROGRESSBAR ___________________________________________________________________________
mat_accu_fig = Figure(figsize=(5.8, 6.36), dpi=80)
mat_accu_fig.patch.set_facecolor('gray')
mat_accu_fig.subplots_adjust(bottom=0.14)
mat_accu_can = FigureCanvasTkAgg(mat_accu_fig)
mat_accu_can.get_tk_widget().place(x=33, y=169)
mat_accu_sub = mat_accu_fig.add_subplot()
mat_accu_sub.set_facecolor('gray')
mat_accu_sub.axis('off')

mat_stock_fig = Figure(figsize=(4.48, 2.8), dpi=80)
mat_stock_fig.patch.set_facecolor('gray')
mat_stock_fig.subplots_adjust(bottom=0.2)
mat_stock_can = FigureCanvasTkAgg(mat_stock_fig)
mat_stock_can.get_tk_widget().place(x=526, y=169)
mat_stock_sub = mat_stock_fig.add_subplot()
mat_stock_sub.set_facecolor('gray')
mat_stock_sub.axis('off')

speed_fig = Figure(figsize=(4.48, 2.37), dpi=80)
speed_fig.patch.set_facecolor('gray')
speed_fig.subplots_adjust(bottom=0.2)
speed_can = FigureCanvasTkAgg(speed_fig)
speed_can.get_tk_widget().place(x=526, y=488, bordermode=OUTSIDE)
speed_sub = speed_fig.add_subplot()
speed_sub.set_facecolor('gray')
speed_sub.axis('off')

progress_mat = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")
progress_stock = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")
progress_speed = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")


def set_dia_settings():
    # MATERIAL:
    mat_accu_sub.set_xticks([_ for _ in range(0, 3601, 120)])

    mat_accu_sub.tick_params(axis='x', labelrotation=90)

    mat_accu_sub.set_yticks([10, 17, 25, 33, 41, 49, 57, 67])

    mat_accu_sub.set(xlabel='sec', ylabel='mm')

    mat_accu_sub.axis('on')

    # SPEED:
    speed_sub.set_xticks([_ for _ in range(0, 61, 10)])

    speed_sub.tick_params(axis='x', labelrotation=0)

    speed_sub.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    speed_sub.set(xlabel='min', ylabel='mm/s')

    speed_sub.axis('on')

    # STOCK:
    mat_stock_sub.set_xticks([_ for _ in range(0, 61, 10)])
    mat_stock_sub.set_yticks(list(set_y_float_ticks(0, 4, '0.5')))

    mat_stock_sub.set(xlabel='min', ylabel='m²')

    mat_stock_sub.axis('on')


def set_y_float_ticks(y0, yn, step):
    while y0 < yn:
        yield float(y0)
        y0 += decimal.Decimal(step)


def download_df_aws():
    client = boto3.client('iotanalytics', region_name='eu-central-1')

    df_aws = client.get_dataset_content(datasetName='qc_glass_production_dataset')

    df = pd.read_csv(df_aws["entries"][0]["dataURI"])

    # Columns:
    for _ in df:
        if _ not in ['ldr_grau', 'ldr_weiss', 'ldr_blau', 'ldr_gelb', 'ldr_lila', 'ldr_gruen', 'date', 'time',
                     'rotation_time', 'distance']:
            df = df.drop(_, axis=1)

    # Rows:
    df = df[df['date'].notna()]
    df = df.sort_values(by=['time'])

    # Filter current day:
    df = df[(df['date'] == str(datetime.date.today()))]

    # Sort by time:
    df = df.sort_values(by=['time'])

    # Duplicates:
    fil = list(df.duplicated(subset=['time'], keep='first'))

    for i in range(0, len(fil)):
        if fil[i] is False:
            fil[i] = True
        else:
            fil[i] = False

    df = df[fil]

    return df


def new_df():
    global after_id

    if p['counter'] > 0:

        prod_laufzeit_lbl['text'] = p['counter']

        df_aws = download_df_aws()
        df_aws_tail = df_aws.tail(60)
        df_aws_tail.reset_index(drop=True, inplace=True)

        update_mat_data(df_aws_tail[['ldr_weiss', 'ldr_grau', 'ldr_lila', 'ldr_blau', 'ldr_gruen', 'ldr_gelb']])
        update_speed_data(df_aws_tail[['rotation_time', 'distance']])
        update_stock_data(df_aws_tail)
        update_label()

        plot_subs()

        data_to_csv(df_aws, df_aws_tail)

    p['counter'] += 1

    after_id = window.after(d['update_time'], new_df)


def data_to_csv(df_aws, df_aws_tail):

    df_aws.to_csv('src/df_aws.csv')

    df_mat_new = pd.DataFrame({'x_values_min_mat': d['x_values_min_mat'], 'y_mat':d['y_mat']})
    df_mat_saved = pd.read_csv('src/df_mat.csv', index_col=[0])
    df_mat = df_mat_saved.append(df_mat_new)
    df_mat.to_csv('src/df_mat.csv')
    # df_mat_new.to_csv('src/df_mat.csv')

    df_speed_new = pd.DataFrame({'x_values_min_speed': d['x_values_min_speed'], 'y_speed':d['y_speed']})
    df_speed_saved = pd.read_csv('src/df_speed.csv', index_col=[0])
    df_speed = df_speed_saved.append(df_speed_new)
    df_speed.to_csv('src/df_speed.csv')
    # df_speed_new.to_csv('src/df_speed.csv')

    df_stock_new = pd.DataFrame({'x_values_min_stock': d['x_values_min_stock'], 'y_stock':d['y_stock']})
    df_stock_saved = pd.read_csv('src/df_stock.csv', index_col=[0])
    df_stock = df_stock_saved.append(df_stock_new)
    df_stock.to_csv('src/df_stock.csv')
    # df_stock_new.to_csv('src/df_stock.csv')

    df_ldr_saved = pd.read_csv('src/df_ldr.csv', index_col=[0])
    df_ldr = df_ldr_saved.append(df_aws_tail)
    df_ldr.to_csv('src/df_ldr.csv')
    # df_ldr.to_csv('src/df_ldr.csv')

    # Volt_Setting:
    for _ in df_aws_tail[['ldr_weiss', 'ldr_grau', 'ldr_lila', 'ldr_blau', 'ldr_gruen', 'ldr_gelb']]:
        vs[_] = int(np.nanmean(df_aws_tail[['ldr_weiss', 'ldr_grau', 'ldr_lila', 'ldr_blau', 'ldr_gruen', 'ldr_gelb']][_]))

    df_vs_new = pd.DataFrame(vs, index=[i for i in range(0, p['counter'])])
    df_vs_saved = pd.read_csv('src/df_vs.csv', index_col=[0])
    df_vs = df_stock_saved.append(df_vs_new)
    df_vs.to_csv('src/df_stock.csv')
    # df_vs_new.to_csv('src/df_vs.csv')

    df_oee = pd.DataFrame({'performance': k['performance'], 'availability': k['availability'], 'quality': k['quality'], 'oee': k['oee']}, index=[i for i in range(0, p['counter'])])
    df_oee.to_csv('src/df_oee.csv')


def update_mat_data(df_aws_tail):

    df_aws_tail_mat = df_aws_tail.astype('int32')

    for z in range(0, 60):

        for c in df_aws_tail_mat:

            if (vs[c]-spec['iO']) <= df_aws_tail_mat.loc[z, c] <= (vs[c]+spec['iO']):
                d['ms'].append(0)
                d['col'].append('white')

            else:
                if (vs[c]-spec['low']) <= df_aws_tail_mat.loc[z, c] <= (vs[c]+spec['low']):
                    d['ms'].append(d['dot_size_low'])
                    d['col'].append('white')

                    k['low_def_lbl'] += 1

                else:
                    if (vs[c] - spec['medium']) <= df_aws_tail_mat.loc[z, c] <= (vs[c] + spec['medium']):
                        d['ms'].append(d['dot_size_medium'])
                        d['col'].append('orange')

                        k['medium_def_lbl'] += 1

                    else:
                        d['ms'].append(d['dot_size_high'])
                        d['col'].append('red')

                        k['high_def_lbl'] += 1

            if c == 'ldr_gelb':
                d['y_mat'].append(17)

            elif c == 'ldr_gruen':
                d['y_mat'].append(25)

            elif c == 'ldr_grau':
                d['y_mat'].append(33)

            elif c == 'ldr_blau':
                d['y_mat'].append(41)

            elif c == 'ldr_weiss':
                d['y_mat'].append(49)

            elif c == 'ldr_lila':
                d['y_mat'].append(57)


            if p['counter'] == 1:
                d['x_values_min_mat'].append(z+1)

            else:
                d['x_values_min_mat'].append(z+1+60*(p['counter']-1))


def update_speed_data(df_aws_tail):

    global distance_center

    df_aws_tail_mat = df_aws_tail.astype('int32')

    rotation_time_filter = list(df_aws_tail.duplicated(subset=['rotation_time'], keep='first'))

    for i in range(0, len(rotation_time_filter)):
        if rotation_time_filter[i] is False:
            rotation_time_filter[i] = True
        else:
            rotation_time_filter[i] = False

    rotation_values = df_aws_tail[rotation_time_filter]
    rotation_values.reset_index(drop=True, inplace=True)

    if len(rotation_values) > 0:
        for _ in range(0, len(rotation_values)):
            d['rotation_cache'].append([rotation_values.loc[_, 'rotation_time'], rotation_values.loc[_, 'distance']])

    if len(d['rotation_cache']) == 1:
        speed = 0

    else:

        if (d['rotation_cache'][-1][0] - d['rotation_cache'][-2][0]) > 0:
            speed = (((2 * np.pi) / (d['rotation_cache'][-1][0] - d['rotation_cache'][-2][0])) * d['rotation_cache'][-1][1])

        else:
            speed = d['y_speed'][-1]

    d['x_values_min_speed'].append(p['counter'])
    d['y_speed'].append(speed)


def update_stock_data(df_aws_tail):

    if (p['counter'] - p['last_update']) == 2:

        new_distance = df_aws_tail.loc[59, 'distance']

        if new_distance > 100:
            new_distance = df_aws_tail.loc[58, 'distance']
        if new_distance > 100:
            new_distance = df_aws_tail.loc[57, 'distance']
        if new_distance > 100:
            new_distance = df_aws_tail.loc[56, 'distance']
        if new_distance > 100:
            new_distance = df_aws_tail.loc[55, 'distance']
        if new_distance > 100:
            new_distance = df_aws_tail.loc[54, 'distance']

        r_x = distance_center - inner_radius - new_distance
        d0 = np.pi*(inner_radius+r_x)
        d1 = np.pi*inner_radius
        s = (d0-d1)/2
        a = d1+s
        a0 = (d1+s)*band_width
        layer_count = int(r_x/paper_thickness)
        a_total = (a0*layer_count*2)*(10**(-6))
        d['y_stock'].append(a_total)

        p['last_update'] = p['counter']

    else:
        if p['counter'] == 0:
            d['y_stock'].append(0)
        else:
            d['y_stock'].append(d['y_stock'][-1])

    d['x_values_min_stock'].append(p['counter'])


def plot_subs():
    mat_accu_sub.clear()
    speed_sub.clear()
    mat_stock_sub.clear()

    # MATERIAL:
    mat_accu_sub.scatter(d['x_values_min_mat'], d['y_mat'], s=d['ms'], color=d['col'])

    mat_accu_sub.vlines([p['counter']*60], 5, 62, linestyles='dashed', colors='blue', alpha=0.5)
    mat_accu_sub.hlines([5], p['counter']*60, 0,  colors='blue', alpha=0.5)
    mat_accu_sub.hlines([62], p['counter']*60, 0,  colors='blue', alpha=0.5)

    # SPEED:
    speed_sub.plot(d['x_values_min_speed'], d['y_speed'], color='yellow')

    # STOCK:
    mat_stock_sub.plot(d['x_values_min_stock'], d['y_stock'], color='blue')

    mat_stock_sub.hlines([0.5], 60, 0, colors='black', linestyles='dashed', alpha=0.5)
    mat_stock_sub.hlines([0.1], 60, 0, colors='red', linestyles='dashed', alpha=0.5)

    set_dia_settings()

    if p['counter'] > 0:
        mat_accu_can.draw()
        mat_stock_can.draw()
        speed_can.draw()


def update_label():
    if len(d['y_speed']) > 0:
        mm_def_lbl['text'] = np.round((k['high_def_lbl'] + k['medium_def_lbl'] + k['low_def_lbl']) / np.round(np.nanmean(d['y_speed'])*1*57, 2))
        speed_lbl['text'] = (np.round(np.nanmean(d['y_speed']), 2))

        prod_flaeche = d['y_speed'][-1] * 60 * 57
        ausschuss = k['high_def_lbl'] * k['high_def_mm'] + k['medium_def_lbl'] * k['medium_def_mm'] + k['low_def_lbl'] * k['low_def_mm']

        k['quality'] = round((prod_flaeche - ausschuss)/prod_flaeche, 4)

        performance_lbl['text'] = k['performance'] * 100.0
        availability_lbl['text'] = k['availability'] * 100.0
        quality_lbl['text'] = round(k['quality'] * 100, 3)

        k['oee'] = int((k['performance'] * k['availability'] * k['quality']) * 100)
        oee_lbl['text'] = k['oee']

    else:
        mm_def_lbl['text'] = 0

        if p['counter'] == 0:
            speed_lbl['text'] = 0
        else:
            speed_lbl['text'] = d['y_speed'][-1]

    high_def_lbl['text'] = k['high_def_lbl']
    medium_def_lbl['text'] = k['medium_def_lbl']
    low_def_lbl['text'] = k['low_def_lbl']
    total_def_lbl['text'] = k['high_def_lbl'] + k['medium_def_lbl'] + k['low_def_lbl']


def progessbar_read_bytes():

    global max_bytes, progress

    progress += 1000

    progress_mat["value"] = progress
    progress_stock["value"] = progress
    progress_speed["value"] = progress

    progress_mat.update()
    progress_stock.update()
    progress_speed.update()

    if progress < max_bytes:
        stop_cmd['state'] = 'disabled'
        stop_cmd.config(bg='gray95')

        window.after(31, progessbar_read_bytes)

    else:
        stop_cmd['state'] = 'normal'
        stop_cmd.config(bg='red2')

        progress_mat.place_forget()
        progress_stock.place_forget()
        progress_speed.place_forget()

        set_dia_settings()

        mat_accu_can.draw()
        mat_stock_can.draw()
        speed_can.draw()


def reset():
    global progress

    progress = 0

    p['counter'] = 0

    d['ms'].clear()
    d['ms'].append(0)
    d['col'].clear()
    d['col'].append('white')

    k['high_def_lbl'] = 0
    k['medium_def_lbl'] = 0
    k['low_def_lbl'] = 0
    k['total_def_lbl'] = 0

    d['mm_def'] = 0

    d['x_values_min_mat'] = [0]
    d['x_values_min_speed'] = [0]
    d['x_values_min_stock'] = [0]
    d['y_mat'] = [0]
    d['y_speed'] = [0]
    d['y_stock'] = [0]

    mm_def_lbl['text'] = '0'

    high_def_lbl['text'] = '0'
    medium_def_lbl['text'] = '0'
    low_def_lbl['text'] = '0'
    total_def_lbl['text'] = '0'

    speed_lbl['text'] = '0'

    performance_lbl['text'] = '0'
    availability_lbl['text'] = '0'
    quality_lbl['text'] = '0'
    oee_lbl['text'] = '0'

    prod_start_lbl['text'] = ''
    prod_laufzeit_lbl['text'] = ''
    prod_ende_lbl['text'] = ''

    mat_accu_sub.clear()
    mat_stock_sub.clear()
    speed_sub.clear()


def start():
    global max_bytes, progress

    if p['counter'] > 0:
        reset()

        stop_cmd['state'] = 'normal'
        stop_cmd.config(bg='red2')

    prod_start_lbl['text'] = '%0.2d' % localtime()[3] + ':' + '%0.2d' % localtime()[4]
    prod_laufzeit_lbl['text'] = p['counter']

    start_cmd['state'] = 'disabled'
    start_cmd.config(bg='gray95')

    progress_mat.place(x=167, y=420)
    progress_stock.place(x=600, y=273)
    progress_speed.place(x=600, y=573)

    progress_mat["value"] = 0
    progress_stock["value"] = 0
    progress_speed["value"] = 0

    progress_mat["maximum"] = max_bytes
    progress_stock["maximum"] = max_bytes
    progress_speed["maximum"] = max_bytes

    progessbar_read_bytes()

    new_df()


def stop():
    global after_id

    if after_id:

        prod_ende_lbl['text'] = '%0.2d' % localtime()[3] + ':' + '%0.2d' % localtime()[4]

        start_cmd['state'] = 'normal'
        start_cmd.config(bg='spring green')

        stop_cmd['state'] = 'disabled'
        stop_cmd.config(bg='gray95')

        window.after_cancel(after_id)

        after_id = None


stop_cmd['state'] = 'disabled'
stop_cmd.config(bg='gray95')

start_cmd.config(command=start)
stop_cmd.config(command=stop)

window.mainloop()
