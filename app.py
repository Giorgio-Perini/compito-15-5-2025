from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
FILE = 'prenotazioni.csv'
SPORTS = ['Calcio', 'Tennis', 'Basket', 'Pallavolo']


# Home
@app.route('/')
def home():
    return render_template('home.html')


# Elimina prenotazione
@app.route('/elimina', methods=['POST'])
def elimina():
    da_eliminare = int(request.form['elimino'])
    df = pd.read_csv(FILE)
    df2 = df[df.index != da_eliminare] # Elimina la riga con l'indice specificato
    df2.to_csv(FILE, index=False)
    return visualizza()


# Visualizza prenotazioni
@app.route('/visualizza', methods=['GET'])
def visualizza():
    df = pd.read_csv(FILE)
    prenotazioni = df.to_dict('records')
    return render_template('visualizza.html', prenotazioni=prenotazioni)


# Aggiungi prenotazione
@app.route('/aggiungi', methods=['GET', 'POST'])
def aggiungi():
    errore = ''
    if request.method == 'POST':
        nome = request.form['nome']
        sport = request.form['sport']
        data = request.form['data']
        ora = request.form['ora']
        note = request.form['note']


        df = pd.read_csv(FILE)
        df.loc[len(df)] = [nome, sport, data, ora, note] # Aggiunge una nuova riga alla fine del DataFrame
        df.to_csv(FILE, index=False)
        return visualizza()
    

    return render_template('aggiungi.html', sports=SPORTS, errore=errore)


# cerca prenotazione
@app.route('/cerca', methods=['GET', 'POST'])
def cerca():
    errore = ''
    prenotazioni = None
    if request.method == 'POST':
        nome = request.form['nome']
        df = pd.read_csv(FILE)
        prenotazioni = df[df['nome'] == nome].to_dict('records')
        if not prenotazioni:
            errore = 'Nessuna prenotazione trovata'
    return render_template('cerca.html', prenotazioni=prenotazioni, errore=errore)


if __name__ == '__main__':
    app.run(debug=True)