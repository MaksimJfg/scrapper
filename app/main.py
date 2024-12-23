from flask import Flask, render_template, request
from scrap import get_data, create_table

app = Flask(__name__)



@app.route("/")
def show_drinks():
    drinks = get_data("SELECT drinktype, name, price, color, region, sugar, grape, manufacture, strength, volume, whiskey_type, alcohol, priceforliter, linktodrink FROM Drinks")
    drinktypes = sorted({drink[0] for drink in drinks})
    colors = sorted({drink[3] for drink in drinks})
    sugars = sorted({drink[5] for drink in drinks})
    whiskey_types = sorted({drink[10] for drink in drinks if drink[10]})

    return render_template('index.html', drinks=drinks, drinktypes=drinktypes, colors=colors, sugars=sugars,
                           whiskey_types=whiskey_types)


if __name__ == "__main__":
    create_table()
    app.run(debug=True, host="0.0.0.0", port=5000)