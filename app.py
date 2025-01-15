from flask import Flask, render_template, request
from datetime import datetime, timedelta
import math

app = Flask(__name__)

@app.route('/')
def index():
    """
    Hoofdpagina met invoervelden.
    """
    return render_template('index.html')

@app.route('/bereken', methods=['POST'])
def bereken():
    """
    Verwerkt de POST-data vanuit het formulier en toont de resultaten.
    """
    # 1. Ophalen van de form-data
    cb_bol_7 = float(request.form.get('cb_bol_7', 0))
    cb_overig_7 = float(request.form.get('cb_overig_7', 0))
    webshop_7 = float(request.form.get('webshop_7', 0))
    retour_percentage = float(request.form.get('retour_percentage', 10)) / 100  # standaard 10%
    gemiddelde_maandverkoop = float(request.form.get('gemiddelde_maandverkoop', 0))
    kosten_per_eenheid = float(request.form.get('kosten_per_eenheid', 2))  # standaardkosten per eenheid
    verkoopprijs = float(request.form.get('verkoopprijs', 20))

    # 2. Huidige voorraad
    voorraad_cb = float(request.form.get('voorraad_cb', 0))
    voorraad_webshop = float(request.form.get('voorraad_webshop', 0))

    # 3. Duur herdruk
    duur_herdruk = float(request.form.get('duur_herdruk', 0))

    # 4. Berekeningen
    totaal_verkoop_7dagen = cb_bol_7 + cb_overig_7 + webshop_7
    gem_verkoop_per_dag = totaal_verkoop_7dagen / 7 if totaal_verkoop_7dagen > 0 else 0
    totale_voorraad = voorraad_cb + voorraad_webshop
    dagen_voorraad = totale_voorraad / gem_verkoop_per_dag if gem_verkoop_per_dag > 0 else 999999
    vandaag = datetime.now().date()
    voorraad_op_datum = vandaag + timedelta(days=math.ceil(dagen_voorraad))

    # Voorgestelde oplage op basis van gemiddelde maandverkoop en retourpercentage
    jaarverkoop = gemiddelde_maandverkoop * 12
    netto_verkoopverwachting = jaarverkoop * (1 - retour_percentage)
    break_even_oplage = netto_verkoopverwachting / (verkoopprijs - kosten_per_eenheid)

    voorgestelde_oplage = math.ceil(break_even_oplage)

    # Datum voor starten van herdruk
    herdruk_start = voorraad_op_datum - timedelta(days=int(duur_herdruk))

    # Resultaten
    resultaten = {
        'gem_verkoop_per_dag': round(gem_verkoop_per_dag, 2),
        'dagen_voorraad': round(dagen_voorraad, 1),
        'voorraad_op_datum': voorraad_op_datum.strftime('%d-%m-%Y'),
        'voorgestelde_oplage': voorgestelde_oplage,
        'break_even_oplage': math.ceil(break_even_oplage),
        'herdruk_start': herdruk_start.strftime('%d-%m-%Y')
    }

    return render_template('resultaat.html', resultaten=resultaten)

if __name__ == '__main__':
    app.run(debug=True)