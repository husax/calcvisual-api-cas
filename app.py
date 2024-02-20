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
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def properties(poly):
    x = symbols('x')
    polinL = poly.split(',')
    if len(polinL) == 1:
        pol = polinL[0]
        pol= Poly(pol, x, domain= 'QQ')
        print(pol.rep.rep)
        if len(pol.rep.rep) == 1:
            polLin=pol.rep.rep
            raices = polLin[0] if polLin[0] == 0 else []
            deriv1= Poly(0, x, domain= 'QQ')
            raicesD1 = [0]
            raicesyDer = [0]
            deriv2= Poly(0, x, domain= 'QQ')
            raicesD2 = [0]
            ventanaX=[-10, 10]
        elif len(pol.rep.rep) == 2:
            polLin = pol.rep.rep
            raices = [float(-polLin[1]/polLin[0])]
            deriv1 = diff(pol, x)
            deriv2 = diff(deriv1, x)
            raicesD1 = []
            raicesyDer = raices.copy()
            raicesD2 = [0]
            ventanaX = [floor( -abs(raices[0])*2.0), math.ceil( abs(raices[0])*2.0)]
        elif len(pol.rep.rep) == 3:
            raices = aprox(real_roots(pol))
            deriv1 = diff(pol, x)
            deriv2 = diff(deriv1, x)
            polDer= deriv1.rep.rep
            raicesD1 = [float(-polDer[1]/polDer[0])]
            raicesyDer = raices + raicesD1
            raicesyDer.sort()
            raicesD2 = []
            if len(raicesyDer) > 1:
                ventanaX = [1.1*raicesyDer[0], 1.1*raicesyDer[-1]]
            else:
                ventanaX= [- abs(raicesyDer[0])*2, abs(raicesyDer[0])*2]
            ventanaX[0]= floor(ventanaX[0])
            ventanaX[1]= math.ceil(ventanaX[1])
        else:
            deriv1 = diff(pol, x)
            deriv2 = diff(deriv1, x)
            pol = Poly(pol)
            raices = aprox(real_roots(pol))
            raicesD1 = aprox(real_roots(deriv1))
            der2Pol = Poly(deriv2)
            raicesD2 = aprox(real_roots(der2Pol))
            raicesyDer = raices + raicesD1
            raicesyDer.sort()
            ventanaX = [1.1*raicesyDer[0] - 0.1*raicesyDer[-1], 1.1*raicesyDer[-1] - 0.1*raicesyDer[0]] if (len(raicesyDer) > 1) \
                else [- abs(raicesyDer[0])*1.2, abs(raicesyDer[0])*1.2]
            ventanaX[0] = floor(ventanaX[0]) if ventanaX[0] < 0 else -10
            ventanaX[1] = math.ceil(ventanaX[1]) if ventanaX[1] > 0 else 10
        return {
            "racional": format(false),
            "polinomio": {
                "expr": format(pol.as_expr()),
                "latex": latex(pol.as_expr()),
            },
            "derivada": {
                "expr": format(deriv1.as_expr()),
                "latex": latex(deriv1.as_expr()),
            },
            "derivada2": {
                "expr": format(deriv2.as_expr()),
                "latex": latex(deriv2.as_expr()),
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
        polNum = Poly(polNum, x, domain='QQ')
        polDen = Poly(polDen, x, domain='QQ')
        raices = aprox(real_roots(polNum))
        raices.sort()
        polos = aprox(real_roots(polDen))
        polosOrig= polos.copy()
        polos.sort()
        remov = discontRemov(raices, polos)
        rac = polNum/polDen
        derNum = diff(polNum, x)*polDen-polNum*diff(polDen, x)
        deriv1 = diff(rac, x)
        junDeriv = together(deriv1)
        deriv2 = diff(deriv1, x)
        der2Num = diff(derNum, x)*polDen**2 - \
            2*polDen*diff(polDen, x)*derNum
        raicesD1 = aprox(real_roots(derNum))
        polosD1= polosOrig + polosOrig
        polosD2= polosD1 + polosD1
        polosD1.sort()
        polosD2.sort
        removD1= discontRemov(raicesD1, polosD1)
        #raicesD1 = quitaRemov(raicesD1, remov)    
        raicesD2 = aprox(real_roots(der2Num))
        removD2= discontRemov(raicesD2, polosD2)
        polosRaicesyDer = polos + raices
        polosRaicesyDer = polosRaicesyDer + raicesD1
        polosRaicesyDer.sort()
        ventanaX = [1.1*polosRaicesyDer[0] - 0.1*polosRaicesyDer[-1],   1.1*polosRaicesyDer[-1] - 0.1*polosRaicesyDer[0]] if len(polosRaicesyDer) > 1 \
            else [- abs(polosRaicesyDer[0])*1.2, abs(polosRaicesyDer[0])*1.2]
        ventanaX[0] = floor(ventanaX[0]) if ventanaX[0] < 0 else -5
        ventanaX[1] = math.ceil(ventanaX[1]) if ventanaX[1] > 0 else 5
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
    return {"error": "hubo error al calcular con la expresión"}

# 
def aprox(raices):
    rAprox = []
    for r in raices:
        if isinstance(r, Rational):
            rAprox.append(r)
        else:
            rAprox.append(r.evalf(15))
    return rAprox

# Remueve en raices y polos los valores comunes 
# que corresponden a discontinuidades removibles. 
# Toma en cuenta las multiplicidades
# Ojo: modifica ambos arreglos
def discontRemov(raices, polos):
    aRemov = []
    for r in raices:
        for p in polos:
            if r == p:
                aRemov.append(r)
                polos.remove(p)
                break
    for item in aRemov:
        raices.remove(item);            
    return aRemov

if __name__ == '__main__':
    app.run(debug=True)
