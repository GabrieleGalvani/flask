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

stazioni = pd.read_csv('/workspace/flask/Verifica1B/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')
stazionigeo = gpd.read_file('/workspace/flask/Verifica1B/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/flask/Verifica1B/ds964_nil_wm.zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/scelta', methods=['GET'])
def scelta():
    quartieri_ordine = quartieri.NIL.to_list()
    quartieri_ordine = list(set(quartieri_ordine))
    quartieri_ordine.sort()
    return render_template('scelta.html', quartieri = quartieri_ordine)

@app.route('/stazioniradio', methods=['GET'])
def stazioniradio():
    quartieriRadio = request.args['quartiere']
    quartiere_utente = quartieri[quartieri['NIL'] == quartieriRadio]
    stazioni_quartieri = stazionigeo[stazionigeo.within(quartiere_utente.geometry.squeeze())]
    return render_template('elenco.html', risultato = stazioni_quartieri.to_html())

@app.route('/nome', methods=['GET'])
def nome():
    return render_template('nome.html')

@app.route('/risultato', methods=['GET'])
def risultato():
    global quartiereUtente, stazioniQuartieri
    quartiere = request.args['quartiere']
    quartiereUtente = quartieri[quartieri['NIL'].str.contains(quartiere)]
    stazioniQuartieri = stazionigeo[stazionigeo.within(quartiereUtente.geometry.squeeze())]
    return render_template('mappa.html')

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))
    quartiereUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    stazioniQuartieri.to_crs(epsg=3857).plot(ax=ax, color='k')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/numero', methods=['GET'])
def numero():
  global risultato
  risultato = stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index().sort_values(by='MUNICIPIO',ascending=True)
  return render_template('numero.html', risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
  fig, ax = plt.subplots(figsize=(12,8))
  x = risultato.MUNICIPIO
  y = risultato.OPERATORE
  ax.bar(x, y, color = "#304C89")
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)