from flask import Flask
# from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import sympy
from sympy import *
import math

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
@cross_origin(origin='http://localhost:8080', headers=['Content-Type', 'Authorization'])
def properties(poly):
    x = symbols('x')
    polinL = poly.split(',')
    if len(polinL) == 1:
        pol = polinL[0]
        deriv1 = diff(pol, x)
        deriv2 = diff(deriv1, x)
        raices = aprox(real_roots(pol))
        raicesD1 = aprox(real_roots(deriv1))
        raicesD2 = aprox(real_roots(deriv2))
        raicesyDer= raices + raicesD1
        raicesyDer.sort()
        ventanaX = [1.1*raicesyDer[0] - 0.1*raicesyDer[-1], 1.1*raicesyDer[-1] - 0.1*raicesyDer[0]] if (len(raicesyDer) > 1) \
            else [- abs(raicesyDer[0])*1.2, abs(raicesyDer[0])*1.2]
        ventanaX[0]= floor(ventanaX[0]) if ventanaX[0] < 0 else -5
        ventanaX[1]= math.ceil(ventanaX[1]) if ventanaX[1] > 0 else 5
        return {
            "racional": format(false),
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
                "rfun": format(raices),
                "rder1": format(raicesD1), 
                "rder2": format(raicesD2),
            },
            "ventanaX": format(ventanaX),
        }
    elif len(polinL) == 2:
        polNum, polDen = polinL
        polNum = Poly(polNum, x, domain= 'QQ')
        polDen = Poly(polDen,x, domain='QQ')
        raices = aprox(real_roots(polNum))
        polos = aprox(real_roots(polDen))
        remov = discontRemov(raices, polos)
        raices = quitaRemov(raices, remov)
        polos = quitaRemov(polos, remov)
        rac = polNum/polDen
        derNum = diff(polNum, x)*polDen-polNum*diff(polDen, x)
        deriv1 = diff(rac, x)
        junDeriv= together(deriv1)
        deriv2 = diff(deriv1, x)
        der2Num = diff(derNum, x)*polDen**2 - \
            2*polDen*diff(polDen, x)*derNum
        raicesD1 = quitaRemov(aprox(real_roots(derNum)), remov)
        raicesD2 = quitaRemov(aprox(real_roots(der2Num)), remov)
        polosRaicesyDer= polos + raices
        polosRaicesyDer= polosRaicesyDer + raicesD1
        polosRaicesyDer.sort()
        ventanaX = [1.1*polosRaicesyDer[0] - 0.1*polosRaicesyDer[-1],   1.1*polosRaicesyDer[-1] - 0.1*polosRaicesyDer[0]] if len(polosRaicesyDer) > 1 \
            else [- abs(polosRaicesyDer[0])*1.2, abs(polosRaicesyDer[0])*1.2]
        ventanaX[0]= floor(ventanaX[0]) if ventanaX[0] < 0 else -5
        ventanaX[1]= math.ceil(ventanaX[1]) if ventanaX[1] > 0 else 5
        return {
            "racional": format(true),
            "polNum": {
                "expr": format(polNum.as_expr()),
                "latex": latex(polNum.as_expr())
            },
            "polDen": {
                "expr": format(polDen.as_expr()),
                "latex": latex(polDen.as_expr())
            },
            "derivada": {
                "expr": format(deriv1),
                "latex": latex(junDeriv)
            },
            "derivada2": {
                "expr": format(deriv2),
                "latex": latex(deriv2)
            },
            "raices": {
                "rfun": format(raices),
                "rder1": format(raicesD1),
                "rder2": format(raicesD2)
            },
            "polos": format(polos),
            "remov": format(remov),
            "ventanaX": format(ventanaX),
            "polosRaicesyDer": format(polosRaicesyDer),
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

def discontRemov(raices, polos):
    remov= []
    for r in raices:
        for p in polos:
            if r == p:
                remov.append(r)
    return remov


def quitaRemov(arr, remov):
    result= arr.copy()
    for item in remov:
        while True:
            try:
                result.remove(item)
            except ValueError:
                break        
    return result
    




if __name__ == '__main__':
    app.run(debug=True)
