from flask import Flask, render_template, request, url_for
import pandas as pd
from datetime import datetime
from PIL import Image
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    years = request.form.get('years')
    months = request.form.get('months')
    days = request.form.get('days')

    df = pd.read_csv(f'data/{years}.csv')

    months = int(months)
    days = int(days)
    meisu = df.iloc[days - 1, months]
    meisu = meisu.replace('-','')

    current = datetime.now()
    current_year = current.year
    current_year = int(current_year)

    years = int(years)
    if (years % 2) == 0:
        even_odd = '金'
    else:
        even_odd = '銀'

    global yourType

    age = current_year - years
    if age >= 60:
        wk_meisu = meisu[0:2]
    elif age >= 30:
        wk_meisu = meisu[2:4]
    elif age >= 0:
        wk_meisu = meisu[4:6]
    else:
        pass

    wk_type = ''
    if wk_meisu < '11':
        wk_type = '羅針盤'
    elif wk_meisu < '21':
        wk_type = 'インディアン'
    elif wk_meisu < '31':
        wk_type = '鳳凰'
    elif wk_meisu < '41':
        wk_type = '時計'
    elif wk_meisu < '51':
        wk_type = 'カメレオン'
    elif wk_meisu < '61':
        wk_type = 'イルカ'
    else:
        pass

    if wk_type == '':
        print('その他')
    else:
        print(f'あなたは{even_odd}の{wk_type}型です。')
        yourType = f'{even_odd}の{wk_type}{wk_meisu}'

    img_path = f'static/img/{yourType[0:-2]}.png'
    with open(f'2022/{yourType[0:-2]}.txt', 'r', encoding='utf-8') as f:
        unsei2022 = f.read()

    return render_template('result.html',
                           age=age,
                           yourType=yourType[0:-2],
                           picture=img_path,
                           unsei2022=unsei2022
    )

if __name__ == '__main__':
    app.run(debug=True)
