from flask import Flask, request, render_template
import gspread



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/test', methods=['POST'])
def receive_text():
    text = request.form['text_to_send']
    text = text.replace('"', '')
    text = text.replace(',', '')
    text = text.replace('[ColorCode', '')
    text = text.replace(']', '')
    
    sa = gspread.service_account(filename="credintials.json")
    sh = sa.open("ESP_Data_Portal")
    wks = sh.worksheet("Sheet1")
    wks.update('A1', text)
    return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
