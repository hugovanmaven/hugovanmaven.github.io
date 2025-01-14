from flask import Flask, render_template, request
from datetime import datetime, timedelta

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
    
    # Optioneel
    datum_publicatie = request.form.get('datum_publicatie', '')
    totaal_verkocht = request.form.get('totaal_verkocht', '')
    
    # 2. Huidige voorraad
    voorraad_cb = float(request.form.get('voorraad_cb', 0))
    voorraad_webshop = float(request.form.get('voorraad_webshop', 0))
    
    # 3. Duur herdruk
    duur_herdruk = float(request.form.get('duur_herdruk', 0))
    
    # 4. AI-enhanced (checkbox)
    ai_enhanced = request.form.get('ai_enhanced', 'off') == 'on'
    
    # 5. Basisberekeningen
    # Gemiddelde verkoop per dag (op basis van laatste 7 dagen)
    totaal_verkoop_7dagen = cb_bol_7 + cb_overig_7 + webshop_7
    if totaal_verkoop_7dagen == 0:
        gem_verkoop_per_dag = 0
    else:
        gem_verkoop_per_dag = totaal_verkoop_7dagen / 7
    
    # Totale voorraad
    totale_voorraad = voorraad_cb + voorraad_webshop
    
    # Aantal dagen voorraad
    if gem_verkoop_per_dag == 0:
        dagen_voorraad = 999999  # als er geen verkoop is, 'oneindig' :-)
    else:
        dagen_voorraad = totale_voorraad / gem_verkoop_per_dag
    
    # Datum dat voorraad opraakt
    vandaag = datetime.now().date()
    voorraad_op_datum = vandaag + timedelta(days=int(dagen_voorraad))
    
    # Voorstel voor oplage (sterk vereenvoudigd)
    if ai_enhanced:
        # Met "AI" houden we zogenaamd rekening met trends
        # (In het echt zou je hier een AI-model aanroepen / logica gebruiken)
        factor = 14  # 2 weken extra voorraad, maar we doen net alsof AI het verhoogt
    else:
        factor = 7   # 1 week extra voorraad
    
    # Eventueel meenemen van "verkoop sinds publicatie"
    # We doen alsof we deze info gebruiken om de factor iets te verhogen.
    # In het echt kun je hier allerlei AI- of business-logica op loslaten.
    if totaal_verkocht:
        try:
            totaal_verkocht = float(totaal_verkocht)
            # symbolische aanpassing: als het boek zeer goed verkocht heeft
            if totaal_verkocht > 1000:
                factor += 3
        except ValueError:
            pass  # als de gebruiker niks of ongeldigs heeft ingevuld, doen we niks
    
    voorgestelde_oplage = int(gem_verkoop_per_dag * factor) if gem_verkoop_per_dag > 0 else 100
    
    # Datum dat de herdruk moet starten
    # Start herdruk x dagen voor de voorraad opraakt
    herdruk_start = voorraad_op_datum - timedelta(days=int(duur_herdruk))
    
    # Resultaten in dict stoppen
    resultaten = {
        'dagen_voorraad': round(dagen_voorraad, 1),
        'voorraad_op_datum': voorraad_op_datum.strftime('%d-%m-%Y'),
        'voorgestelde_oplage': voorgestelde_oplage,
        'herdruk_start': herdruk_start.strftime('%d-%m-%Y')
    }
    
    return render_template('resultaat.html', resultaten=resultaten)

if __name__ == '__main__':
    app.run(debug=True)