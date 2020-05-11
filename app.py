from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import sympy
from sympy import *

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/api/v1/info', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def info():
    x,y = symbols('x,y')
    polynomial = '4*x**2'    
    derivative = format(diff(polynomial, x, 1))
    return {
        "sympy_version": sympy.__version__,
        "polynomial": polynomial,
        "derivative": derivative
        }

@app.route('/api/v1/polynomial/properties/<poly>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def properties(poly):
    x,y = symbols('x,y')
    polynomial = eval(poly)  
    derivative = diff(polynomial, x, 1)
    derivada = diff(polynomial, x, 1)
    derivada2 = diff(diff(polynomial, x),x)
    raices = solve(Eq(polynomial,0),x)
    puntosInflexion = []
    return {
        "polinomio": {
            "expr":format(polynomial),
            "latex":latex(polynomial)
            },
        "derivada":{
            "expr":format(derivada),
            "latex":latex(derivada)
            },
        "derivada2":{
            "expr":format(derivada2),
            "latex":latex(derivada2)
            },
        "raices":{
            "expr":format(raices),
            "latex":latex(raices)
            },
        "puntosInflexion":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "clasifPuntosCriticos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "puntosCriticos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "signoFuncPos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "signoFuncNeg":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "monotoniaPos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "monotoniaNeg":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "concavidadPos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "concavidadNeg":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "extensionPos":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            },
        "extensionNeg":{
            "expr":format(puntosInflexion),
            "latex":latex(puntosInflexion)
            }
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')