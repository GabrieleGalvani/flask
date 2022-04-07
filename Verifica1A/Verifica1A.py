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

stazioni = pd.read_csv('/workspace/flask/Verifica1A/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')
stazionigeo = gpd.read_file('/workspace/flask/Verifica1A/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/flask/Verifica1A/ds964_nil_wm.zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('home1.html')

@app.route('/numero', methods=['GET'])
def numero():
  global risultato
  risultato = stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index().sort_values(by='MUNICIPIO',ascending=True)
  return render_template('link1.html', risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
  # Costruzione del grafico
  fig, ax = plt.subplots(figsize=(12,8))
  x = risultato.MUNICIPIO
  y = risultato.OPERATORE
  ax.bar(x, y, color = "#304C89")
  # Visualizzazione del grafico
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'es1':
    return redirect(url_for('numero'))
  elif scelta == 'es2':
    return redirect(url_for('input'))
  else:
    return redirect(url_for('dropdown'))

@app.route('/input', methods=['GET'])
def input():
  return render_template('input.html')

@app.route('/ricerca', methods=['GET'])
def ricerca():
    global quartiere, stazioni_quartiere
    quartiere = request.args['quartieri']
    quartiereUtente = quartieri[quartieri['NIL'].str.contains(quartiere)]
    stazioniQuartieri = stazionigeo[stazionigeo.within(quartiereUtente.geometry.squeeze())]
    return render_template('elenco.html', risultato = stazioniQuartieri.to_html())


 
@app.route("/mappa", methods=["GET"])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    stazioni_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/dropdown', methods=['GET'])
def dropdown():
    nomi_stazioni = stazioni.OPERATORE.to_list()
    nomi_stazioni = list(set(nomi_stazioni))
    nomi_stazioni.sort()
    return render_template("dropdown.html", stazioni = nomi_stazioni)

@app.route('/sceltastazione', methods=['GET'])
def sceltastazione():
    global quartiere1, stazione_utente
    stazione = request.args['stazione']
    stazione_utente = stazionigeo[stazionigeo.OPERATORE==stazione]
    quartiere1 = quartieri[quartieri.contains(stazione_utente.geometry.squeeze)]
    return render_template("vistastazione.html", quartiere = quartiere)

@app.route('/mappaquart', methods=['GET'])
def mappaquart():
    fig, ax = plt.subplots(figsize = (12,8))

    stazioni_utente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    quartiere1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    return render_template('home1.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)