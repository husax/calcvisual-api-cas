from flask import Flask
from flask_cors import CORS, cross_origin
import sympy
from sympy import *
from sympy.parsing.latex import parse_latex

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

@app.route('/api/v1/polynomial/properties/<polynomial>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def properties(polynomial):
    x,y = symbols('x,y')    
    derivative = diff(polynomial, x, 1)
    return {
        "polinomio": {
            "latex":latex(derivative)
            }        
        }

if __name__ == '__main__':
    app.run()