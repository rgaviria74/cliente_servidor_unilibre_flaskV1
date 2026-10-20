from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "Hola Mundo"
    
@app.route('/paginauno')
def paginauno():
    return  """
             <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>    
                <h1>Primera Pagina</h1>
                <p>Contenido de la Primera Pagina</p>
            </body>
            </html>
            """

@app.route('/paginados')
def paginados():
    return render_template('/paginados.html')

@app.route('/saludo')
def template_saludo():
    nombre="Carvajal"
    return render_template('/saludo.html', nombre=nombre, curso="Programacion Web")

@app.route('/expresiones')
def template_expresiones():
    nombre="Carvajal"
    curso="Programacion Web"
    base = 3
    altura = 5
    return render_template('/expresiones.html', nombre=nombre, curso=curso, base=base, altura=altura)

@app.route('/expresionesmejor')
def template_expresionesmejor():
    kwargs = {
    "nombre": "Carvajal",
    "curso" : "Programacion Web",
    "base" : 3,
    "altura" : 5
    }
    return render_template('/expresiones.html', **kwargs )

if __name__ == '__main__':
    app.run(debug=True)