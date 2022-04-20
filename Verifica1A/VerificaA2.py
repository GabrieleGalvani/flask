from flask import Flask, render_template, request, Response, redirect, url_for
app = Flask(__name__)

import io
import geopandas as gpd
import pandas as pd
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

comuni = gpd.read_file('/workspace/flask/Verifica1A/Com01012021_g_WGS84.zip')
province = gpd.read_file('/workspace/flask/Verifica1A/ProvCM01012021_g_WGS84.zip')
regioni = gpd.read_file('/workspace/flask/Verifica1A/Reg01012021_g_WGS84.zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('home1.html')

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'es1':
    return redirect(url_for('comune'))
  elif scelta == 'es2':
    return redirect(url_for('provincia'))
  else:
    return redirect(url_for('regione'))

@app.route('/comune', methods=['GET'])
def comune():
    return render_template('comune.html')

@app.route('/elenco', methods=['GET'])
def elenco():
    global comuneutente, confini_comune
    comune= request.args['comune']
    comuneutente = comuni[comuni.comune.str.contains(comune)]
    confini_comune= comuni[comuni.touches(comune_utente.geometry.squeeze)].sort_values('comune')
    return render_template('elenco1.html',risultato=confini_comune.to_html())

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    comuneutente.to_crs(epsg=3857).plot(ax=ax, facecolor='none', edgecolor="b")
    confini_comune.to_crs(epsg=3857).plot(ax=ax,facecolor='k')
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/provincia', methods=['GET'])
def provincia():
    
    return render_template('provincia.html', province=province['provincia'].drop_duplicates())


@app.route('/scelta_comune', methods=['GET'])
def comune2():
    global comune_utente2, confini_comune2
    comune = request.args['comune']
    comuneutente2 = comuni[comuni.comune.str.contains(comune)
    confini_comune2 = comuni[comuni.touches[comune_utente2.geometry.squeeze()]].sort_values('comune')
    return render_template('elenco2.html', risultato = confini_comune2.to_html())

@app.route('/mappa2', methods=['GET'])
def mappa2():
    fig, ax = plt.subplots(figsize = (12,8))

    comuneutente2.to_crs(epsg=3857).plot(ax=ax, facecolor='none', edgecolor="b")
    confini_comune2.to_crs(epsg=3857).plot(ax=ax,facecolor='k')
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


















if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)