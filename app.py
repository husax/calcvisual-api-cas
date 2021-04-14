from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import sympy
from sympy import *

app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/v1/info', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def info():
    x, y = symbols('x,y')
    polynomial = '4*x**2'
    derivative = format(diff(polynomial, x, 1))
    return {
        "sympy_version": sympy.__version__,
        "polynomial": polynomial,
        "derivative": derivative
    }


@app.route('/api/v1/polynomial/properties/<path:poly>', methods=['GET'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'])
def properties(poly):
    x = symbols('x')
    polinL = poly.split(',')
    if len(polinL) == 1:
        pol = Poly(polinL[0])
        deriv1 = diff(pol, x)
        deriv2 = diff(deriv1, x)
        raices = aprox(real_roots(pol))
        raicesD1 = aprox(real_roots(deriv1))
        raicesD2 = aprox(real_roots(deriv2))
        return {
            "polinomio": {
                "expr": format(pol),
                "latex": latex(pol),
            },
            "derivada": {
                "expr": format(deriv1),
                "latex": latex(deriv1),
            },
            "derivada2": {
                "expr": format(deriv2),
                "latex": latex(deriv2),
            },
            "raices": {
                "rpol": format(raices),
                "rder1": format(raicesD1),
                "rder2": format(raicesD2),
            },
        }
    elif len(polinL) == 2:
        polNum, polDen = polinL
        polNum = Poly(polNum)
        polDen = Poly(polDen)
        raices = aprox(real_roots(polNum))
        polos = aprox(real_roots(polDen))
        rac = polNum/polDen
        derNum = diff(polNum, x)*polDen-polNum*diff(polDen, x)
        deriv1 = diff(rac, x)
        deriv2 = diff(deriv1, x)
        der2Num = diff(derNum, x)*polDen**2 - \
            2*polDen*diff(polDen, x)*derNum
        raicesD1 = aprox(real_roots(derNum))
        raicesD2 = aprox(real_roots(der2Num))
        polosyRaices= polos + raices
        polosyRaices.sort()
        ventanaX = [2*polosyRaices[0] - polosyRaices[-1],   2*polosyRaices[-1] - polosyRaices[0]] if (len(polosyRaices) > 1) \
            else [- abs(polosyRaices[0])*1.2, abs(polosyRaices[0])*1.2]
        return {
            "polNum": {
                "expr": format(polNum),
                "latex": latex(polNum)
            },
            "polDen": {
                "expr": format(polDen),
                "latex": latex(polDen)
            },
            "derivada": {
                "expr": format(deriv1),
                "latex": latex(deriv1)
            },
            "derivada2": {
                "expr": format(deriv2),
                "latex": latex(deriv2)
            },
            "raices": {
                "polNum": format(raices),
                "derNum": format(raicesD1),
                "der2Num": format(raicesD2)
            },
            "polos": format(polos),
            "ventanaX": format(ventanaX),
            "polosyRaices": format(polosyRaices),
        }
    else:
        return {"error": "algo salio mal"}


def aprox(raices):
    rAprox = []
    for r in raices:
        if isinstance(r, Rational):
            rAprox.append(r)
        else:
            rAprox.append(r.evalf(15))
    return rAprox


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
