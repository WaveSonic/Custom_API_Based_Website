from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
import requests
URL_CONVERSE = "https://currency-exchange.p.rapidapi.com/exchange"

app = Flask(__name__)
Bootstrap(app)
choose = ["EUR (Євро)", "CHF (Швейцарський франк)", "AZN (Азербайджанський манат)", "ALL (Албанський лек)",
          "BYN (Білоруський рубель)", "BGN (Болгарський лев)", "BAM (Конвертовна марка Боснії і Герцеговини)",
          "GBP (Фунт стерлінгів)", "AMD (Вірменський драм)", "GEL (Грузинський ларі)", "DKK (Данська крона)", "ISK (Ісландська крона)",
          "MDL (Молдовський лей)", "NOK (Норвезька крона)", "MKD (Македонський денар)", "PLN (Польський злотий)",
          "RUB (Російський рубль)", "RON (Румунський лей)", "RSD (Сербський динар)", "TRY (Турецька ліра)", "HUF (Угорський форинт)",
          "UAH (Українська гривня)", "CZK (Чеська крона)", "SEK (Шведська крона)", "LKR (Рупія Шрі-Ланки)", "PHP (Філіппінський песо)",
          "UZS (Узбецький сум)", "TMT (Туркменський манат)", "TJS (Таджицький сомоні)", "SYP (Сирійський фунт)",
          "OMR (Оманський ріал)", "AED (Дирхам ОАЕ)", "MMK (М'янмський к'ят)", "KWD (Кувейтський динар)", "KPW (Північнокорейська вона)",
          "QAR (Катарський ріал)", "JOD (Йорданський динар)", "IRR (Іранський ріал)", "IQD (Іракський динар)", "YER (Єменський ріал)",
          "BHD (Бахрейнський динар)", "USD (Долар США)", "BND (Брунейський долар)", "INR (Індійська рупія)",
          "NPR (Непальська рупія)", "KZT (Казахстанський теньге)", "KGS (Киргизький сом)", "KHR (Камбоджійський рієль)",
          "CNY (Китайський юань)", "MNT (Монгольський тугрик)", "MVR (Мальдівська руфія)", "BTN (Бутанський нгултрум)",
          "PKR (Пакистанська рупія)", "VND (В'єтнамський донг)", "AFN (Афганський афгані)", "SGD (Сінгапурський долар)",
          "JPY (Японська єна)", "THB (Тайський бат)", "MYR (Малайзійський рингіт)", "LBP (Ліванський фунт)",
          "LAK (Лаоський кіп)", "KRW (Південнокорейська вона)", "IDR (Індонезійська рупія)", "ILS (Ізраїльський новий шекель)",
          "BDT (Бангладеська така)", "SAR (Саудівський ріал)", "XOF (Західноафриканський франк)", "XAF (Центральноафриканський франк)",
          "DZD (Алжирський динар)", "AOA (Ангольська кванза)", "BWP (Ботсванська пула)", "BIF (Бурундійський франк)",
          "GHS (Ганський седі)", "GMD (Гамбійський даласі)", "GNF (Гвінейський франк)", "DJF (Франк Джибуті)",
          "ERN (Еритрейська накфа)", "SZL (Свазілендський ліланґені)", "ETB (Ефіопський бир)", "EGP (Єгипетський фунт)",
          "ZMK (Замбійська квача)", "CVE (Ескудо Кабо-Верде)", "KES (Кенійський шилінг)", "KMF (Коморський франк)",
          "CDF (Конголезький франк)", "LRD (Ліберійський долар)", "LYD (Лівійський динар)", "LSL (Лоті Лесото)",
          "MUR (Маврикійська рупія)", "MRO (Мавританська угія)", "MWK (Малавійська квача)", "MGA (Малагасійський аріарі)",
          "MAD (Марокканський дирхам)", "MZN (Мозамбіцький метікал)", "NAD (Намібійський долар)", "NGN (Нігерійська найра)",
          "ZAR (Південноафриканський ранд)", "SSP (Південносуданський фунт)", "RWF (Руандійський франк)", "STN (Добра Сан-Томе і Принсіпі)",
          "SCR (Сейшельська рупія)", "SOS (Сомалійський шилінг)", "SDG (Суданський фунт)", "SLL (Леоне Сьєрра-Леоне)",
          "TZS (Танзанійський шилінг)", "TND (Туніський динар)", "UGX (Угандійський шилінг)", "XCD (Східнокарибський долар)",
          "BSD (Багамський долар)", "BBD (Барбадоський долар)", "BZD (Белізький долар)", "HTG (Гаїтянський гурд)",
          "GTQ (Гватемальський кетсаль)", "HNL (Гондураська лемпіра)", "DOP (Домініканський песо)", "CAD (Канадський долар)",
          "CRC (Костариканський колон)", "CUP (Кубинський песо)", "CUC (Кубинський конвертований песо)", "MXN (Мексиканський песо)",
          "NIO (Нікарагуанська кордоба)", "PAB (Панамське бальбоа)", "TTD (Долар Тринідаду і Тобаго)", "JMD (Ямайський долар)",
          "ARS (Аргентинський песо)", "BOB (Болівійський болівіано)", "BRL (Бразильський реал)", "VES (Суверенний Болівар)",
          "GYD (Гаянський долар)", "COP (Колумбійський песо)", "PYG (Парагвайський гуарані)", "PEN (Перуанський соль)",
          "SRD (Суринамський долар)", "UYU (Уругвайський песо)", "CLP (Чилійський песо)", "AUD (Австралійський долар)",
          "TVD (Долар Тувалу)", "VUV (Вануатський вату)", "NZD (Новозеландський долар)", "PGK (Папуа-Новогвінейська кіна)",
          "WST (Самоанська тала)", "SBD (Долар Соломонових Островів)", "TOP (Тонганська паанга)", "FJD (Фіджійський долар)"]

char = ['']
choose.sort()
def reverse(a, b):
    a, b = b, a
    return a, b



@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        from_ = request.form.get('From')
        to = request.form.get('To')
        fz = request.form.get('fz')
        if fz == '':
            fz = 0
        if from_ == to or from_ == 'Choose...' or to == 'Choose...':
            return render_template('index.html', nav_bar_pos=0, choose=choose, current_from=from_, current_to=to, data=0, result=0)
        else:
            querystring = {"from": from_.split()[0], "to": to.split()[0]}
            headers = {
                "X-RapidAPI-Key": "22c8d7eeafmsh7e2cca32a3dab54p1c791cjsn43cdf2deff88",
                "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
            }
            response = requests.request("GET", URL_CONVERSE, headers=headers, params=querystring)
            result = round(float(response.text)*float(fz),4)
            return render_template('index.html', nav_bar_pos=0, choose=choose, current_from=from_, current_to=to, data=fz, result=result)
    return render_template('index.html', nav_bar_pos=0, choose=choose, current_from='Choose...', current_to='Choose...', data=0, result=0)




@app.route('/table', methods = ['GET', "POST"])
def table():
    if request.method == 'POST':
        from_ = request.form.get('From')
        to = request.form.get('To')
        if from_ == to or from_ == 'Choose...' or to == 'Choose...':
            return render_template('table.html', nav_bar_pos=1, choose=choose)
        else:
            url = "https://alpha-vantage.p.rapidapi.com/query"

            querystring = {"function": "FX_INTRADAY", "interval": "60min", "to_symbol": from_.split()[0], "from_symbol": to.split()[0],
                           "datatype": "json", "outputsize": "compact"}

            headers = {
                "X-RapidAPI-Key": "22c8d7eeafmsh7e2cca32a3dab54p1c791cjsn43cdf2deff88",
                "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            all_data = response.json()['Time Series FX (60min)']
            date = [date for date in all_data]
            return render_template('table.html', nav_bar_pos=1, choose=choose, date=date, data=all_data, current_from=from_, current_to=to)
    return render_template('table.html', nav_bar_pos=1, choose=choose)

app.run(debug=True)
