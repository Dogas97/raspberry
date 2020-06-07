from flask import *

# Remove os Logs
import logging
import os
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

# Caminhos para os dados
pathD = "/home/pi/Desktop/Projecto/data/data.txt"
pathR = "/home/pi/Desktop/Projecto/data_robot/data.txt"

# Retorna a ultima Data guardada
def readLastData():
    file = open(pathD, "r")
    f = file.readline()
    file.close()
    return f

# Retorna o bit das Baterias
def readBatery():
    file = open(pathR, "r")
    f = file.readline()
    file.close()
    
    # BATERIAS
    # F     [          ]
    # E     [||        ] 
    # D     [||||      ]
    # C     [||||||    ]
    # B     [||||||||  ]
    # A     [||||||||||] 

    bat = abs(ord(f[2]) - 70) * 2
    return ("||||||||||")[:bat]

app = Flask(__name__)

@app.route("/")
def index():
    bat = readBatery()
    if (bat == ''):
        return "<center><b>Sem Bateria no Robot</b></center>"
    return render_template("index.html", value=bat)

@app.route("/receive", methods=["POST"])
def receive():
    data = request.form.get("stringData")
    #file = open(pathD, "w+")
    #file.write(data)
    #file.close()
    print(data + " saved to data.")
    if (data[3] == 'R'):
        print("Rebooting...")
        os.system('reboot')
    elif (data[3] == 'S'):
        print("Shuting down...")
        os.system('shutdown now')
    return readLastData()

app.run(host='0.0.0.0', port=80)