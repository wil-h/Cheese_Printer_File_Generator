from flask import Flask, request, render_template
import gspread



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html') 

@app.route('/test', methods=['POST'])
def receive_text():
    text = request.form['text_to_send']
    text = text.replace('"', '')
    text = text.replace(',', '')
    text = text.replace('[ColorCode', '')
    text = text.replace(']', '')
    parts = text.split(".")
    r, g, b = parts[:3]

    r = r.replace(".", '')
    g = g.replace(".", '')

    colorstring = ""

    for i in range(0, len(r), 3):
        r2 = int(r[i:i+3])
        g2 = int(g[i:i+3])
        b2 = int(b[i:i+3])
        # Convert the RGB values to a range of 0-1
        r3, g3, b3 = float(r2), float(g2), float(b2)
        r3, g3, b3 = r3/255, g3/255, b3/255

        Cmax = max(r3, g3, b3)
        Cmin = min(r3, g3, b3)
        t = 1
        s = 1
        t = Cmax - Cmin
        if(t == 0):
            h=0
            l=0
            s=0
        while(t!=0 and s==1):
            if(Cmax == r3):
                h = 60 * (((g3-b3)/t)%6)
            if(Cmax == g3):
                h = 60*(((b3-r3)/t)+2)
            if(Cmax == b3):
                h = 60*(((r3-g3)/t)+4)
            l = (Cmax+Cmin)/2
            s2 = t/(1-abs((2*l)-1))
            l = l*100
            s = s2*100
        if(l<85 and l>15):
            if(h>0):
                if(h>25):
                    if(h>30):
                        if(h>60):
                            if(h>65):
                                if(h>175):
                                    if(h>270):
                                        if(h>285):
                                            if(h>320):
                                                color = "6" #red
                                            if(h<320):
                                                color = "4" #pink
                                        if(h<285):
                                            color = "a" #purple
                                    if(h<270):
                                        color = "0" #blue
                                if(h<175):
                                    color = "9" #green
                            if(h<65):
                                color = "8" #yellow
                        if(h<60):
                            color = "7" #orange
                    if(h<30):
                        color = "5" #brown
                if(h<25):
                    color = "6" #red
            if(s<11):
                color = "3" #gray
        if(l>85):
            color = "2" #white
        if(l<15):
            color = "1" #black
        colorstring = colorstring+color


    sa = gspread.service_account(filename="credintials.json")
    sh = sa.open("ESP_Data_Portal")
    wks = sh.worksheet("Sheet1")
    wks.update('A1', colorstring)
    return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
