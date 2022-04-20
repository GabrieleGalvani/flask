from flask import Flask, render_template
#pip install flask pandas contextily geopandas matplotlib
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("form.html") #serve per restituire una stringa

@app.route('/it', methods=['GET'])
def ciao_mondo():
    return ('<h1>Ciao, Mondo!</h1>') #serve per restituire la funzione

@app.route('/fr', methods=['GET'])
def bonjour():
    return ('<h1>Bonjour, Monde!</h1>')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True) 