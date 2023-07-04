from flask import Flask, flash, render_template, redirect, url_for, request
import pandas as pd
import numpy as np


# base de datos
df_redes = pd.read_csv('datos_redes.csv', sep=',', names = ['fecha', 'n_huecos', 'p_suciedad'] )
df_agua = pd.read_csv('datos_agua.csv', names =  ['fecha','ph', 'oxigeno_disuelto', 'temperatura'])

df_redes = df_redes.iloc[1:,:]
df_agua = df_agua.iloc[1:,:]

df_redes = df_redes.astype({'n_huecos': int, 'p_suciedad': float})
df_agua = df_agua.astype({'ph':float, 'oxigeno_disuelto':float, 'temperatura':float})

df_redes['fecha'] = pd.to_datetime(df_redes['fecha']).dt.date
df_agua['fecha'] = pd.to_datetime(df_agua['fecha']).dt.date


def df_redes_date_query(var, f_i = '2022-01-10', f_f='2022-01-21'):
    f_i = pd.to_datetime(f_i).date()
    f_f = pd.to_datetime(f_f).date()
    df = df_redes.loc[(df_redes['fecha'] >= f_i) & (df_redes['fecha'] <= f_f)]
    return df['fecha'], df[var]

def df_agua_date_query(var,  f_i = '2022-01-10', f_f='2022-01-21'):
    f_i = pd.to_datetime(f_i).date()
    f_f = pd.to_datetime(f_f).date()
    df = df_agua.loc[(df_agua['fecha'] >= f_i) & (df_agua['fecha'] <= f_f)]
    return df['fecha'], df[var]

def save_arr(arr):
    arr = np.array(arr)
    s = '['
    if (len(arr) != 0):
        for i in range(len(arr)-1):
            s = s + str(arr[i]) + ','
        s = s + str(arr[-1])
    s = s + ']'
    return s
def save_arr_date(arr):
    arr = np.array(arr)
    s = '['
    if (len(arr) != 0):
        for i in range(len(arr)-1):
            s = s + "\'" +str(arr[i]) + "\'" + ','
        s = s + "\'" + str(arr[-1]) + "\'"
    s = s + ']'
    return s

    
def save_js(da,dfs):
    file = open("static/js/pages/dashboard8.js", 'w')
    if len(dfs[0]) !=0:
        file.write("var ph_v = ")
        file.write(save_arr(dfs[0]))
        file.write("\n")
        file.write("var ph_labels = ")
        file.write(save_arr_date(da[0].astype(str)))
        file.write("\n")

    if len(dfs[1]) !=0:
        file.write("var ox_v = ")
        file.write(save_arr(dfs[1]))
        file.write("\n")
        file.write("var ox_labels = ")
        file.write(save_arr_date(da[1].astype(str)))
        file.write("\n")

    if len(dfs[2]) !=0:
        file.write("var temp_v = ")
        file.write(save_arr(dfs[2]))
        file.write("\n")
        file.write("var temp_labels = ")
        file.write(save_arr_date(da[2].astype(str)))
        file.write("\n")

    if len(dfs[3]) !=0:
        file.write("var huecos_v = ")
        file.write(save_arr(dfs[3]))
        file.write("\n")
        file.write("var huecos_labels =")
        file.write(save_arr_date(da[3].astype(str)))
        file.write("\n")

    if len(dfs[4]) !=0:
        file.write("var suciedad_v = ")
        file.write(save_arr(dfs[4]))
        file.write("\n")
        file.write("var suciedad_labels = ")
        file.write(save_arr_date(da[4].astype(str)))
        file.write("\n")

    file.close()




# end base de datos

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"



ruta_v='/'

@app.route('/')
def inicio():
    return render_template('index.html', rq = False)

@app.route(ruta_v+'query', methods =['POST', 'GET'])
def index():
    v_agua = ['ph', 'oxigeno_disuelto', 'temperatura']
    v_redes = ['n_huecos', 'p_suciedad']
    f_i = request.form.get('fecha_inicio')
    f_f = request.form.get('fecha_fin')

    df_1 = []
    df_2 = []
    df_3 = []
    df_4 = []
    df_5 = []

    d1 = []
    d2 = []
    d3 = []
    d4 = []
    d5 = []

    if f_i == '':
        f_i = '2022-01-10'
    if f_f == '':
        f_f = '2022-01-21'

    rq = False
    for i in request.form:
        if request.form.get(i) == '1':
            d1, df_1 = df_agua_date_query(v_agua[0], f_i, f_f)
            rq = True
        if request.form.get(i) == '2':
            d2, df_2 = df_agua_date_query(v_agua[1], f_i, f_f)
            rq = True
        if request.form.get(i) == '3':
            d3, df_3 = df_agua_date_query(v_agua[2], f_i, f_f)
            rq = True
        if request.form.get(i) == '4':
            d4, df_4 = df_redes_date_query(v_redes[0], f_i, f_f)
            rq = True
        if request.form.get(i) == '5':
            d5, df_5 = df_redes_date_query(v_redes[1], f_i, f_f)
            rq = True
        
    da = [d1,d2,d3,d4,d5]
    dfs = [df_1, df_2, df_3, df_4, df_5]
    save_js(da, dfs)
    return render_template('index.html', data_fechas = da, data = dfs, rq=rq)


if __name__ == '__main__':
    app.run(port=4000, host="0.0.0.0",debug=True)
