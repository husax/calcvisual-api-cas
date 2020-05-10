# app.py - a minimal flask api using flask_restful
from flask import Flask
from flask_restful import Resource, Api
import sympy
from sympy import *

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    x,y = symbols('x,y')
    polynomial = '4*x**2'    
    derivative = format(diff(polynomial, x, 1))
    def get(self):
        return {
        	"sympy_version": sympy.__version__,
        	"polynomial": self.polynomial,
        	"derivative": self.derivative
        	}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
