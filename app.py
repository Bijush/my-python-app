from flask import Flask, render_template, request
from sympy import symbols, Eq, solve, sympify, pretty
import matplotlib.pyplot as plt
import numpy as np
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    steps = ''
    if request.method == 'POST':
        equation = request.form['equation']
        equation = equation.replace('−', '-').replace('^', '**').replace('²', '**2').replace('³', '**3').replace('X', 'x')
        equation = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)
        equation = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', equation)

        x = symbols('x')
        try:
            if '=' in equation:
                lhs, rhs = equation.split('=')
                eq = Eq(sympify(lhs), sympify(rhs))
            else:
                eq = Eq(sympify(equation), 0)
            sol = solve(eq, x)
            result = f"Solution: {sol}"
            steps = f"Simplified Equation:<br>{pretty(eq)}"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('index.html', result=result, steps=steps)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    message = ''
    filename = ''
    if request.method == 'POST':
        expr = request.form['expression']
        x = symbols('x')
        try:
            expr = expr.replace('−', '-').replace('^', '**').replace('²', '**2').replace('³', '**3').replace('X', 'x')
            expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
            expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)
            y_expr = sympify(expr)
            f = lambda val: float(y_expr.evalf(subs={x: val}))
            x_vals = np.linspace(-10, 10, 400)
            y_vals = [f(val) for val in x_vals]
            plt.figure()
            plt.plot(x_vals, y_vals, label=f"y = {expr}")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Graph')
            plt.grid(True)
            plt.legend()
            filename = 'static/graph.png'
            os.makedirs('static', exist_ok=True)
            plt.savefig(filename)
            plt.close()
        except Exception as e:
            message = f"Graph Error: {str(e)}"
    return render_template('graph.html', image=filename, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
