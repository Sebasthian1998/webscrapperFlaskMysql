from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from scrapping import getScrapping

app = Flask(__name__)
# Mysql Connection
app.config['MYSQL_DATABASE_HOST'] = 'e11wl4mksauxgu1w.cbetxkdyhwsb.us-east-1.rds.amazonaws.com' 
app.config['MYSQL_DATABASE_USER'] = 'd4ntg9175crpvef5'
app.config['MYSQL_DATABASE_PASSWORD'] = 'w4rvphewlfiobwc4'
app.config['MYSQL_DATABASE_DB'] = 'ztew9u250gtrpeq0'
mysql = MySQL(app)
mysql.init_app(app)

#rutas
@app.route('/')
def Index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT DISTINCT Autor FROM Articulo')
    datos = cursor.fetchall()
    print(datos)
    autores=[]
    for dato in datos:
        citaciones=0
        cursor.execute('SELECT Citaciones FROM Articulo where Autor=%s',(dato))
        Citaciones= cursor.fetchall()
        autor={}
        for citacion in Citaciones:
            citaciones=citacion[0]+citaciones
            autor=(dato,citaciones)
        autores.append(autor)
    print(autores)
    cursor.close()
    return render_template('index.html', contacts = autores)

@app.route('/getAutor', methods=['POST'])
def getAutor():
    name = request.form['name']
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Articulo where Autor =%s ',(name))
    data = cursor.fetchall()
    print(data)
    if len(data)==0:
        articulos=getScrapping(name)
        for articulo in articulos:
            print('***')
            print(articulo)
            cursor.execute("INSERT INTO Articulo (Nombre, Citaciones, Año,Autor) VALUES (%s,%s,%s,%s)", (articulo[0], articulo[1], articulo[2],name))
            
        # print(articulos)
        cursor.execute('SELECT * FROM Articulo where Autor =%s ',(name))
        data = cursor.fetchall()
        print(data)
        return render_template('autor.html', articulos = data,autor=name)
    cursor.close()
    return render_template('autor.html', articulos = data,autor=name)

@app.route('/verAutor', methods=['POST'])
def verAutor():
    autor=request.form['autor']
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Articulo where Autor=%s',(autor))
    data= cursor.fetchall()
    print(data)
    cursor.close()
    return render_template('autor.html', articulos = data,autor=autor)


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
    # app.run()

            



