from flask import Flask, render_template, request
from sympy import symbols, Eq, solve, sympify, latex
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    steps = ''
    if request.method == 'POST':
        equation = request.form['equation']
        x = symbols('x')
        try:
            if '=' in equation:
                lhs, rhs = equation.split('=')
                eq = Eq(sympify(lhs), sympify(rhs))
            else:
                eq = Eq(sympify(equation), 0)

            sol = solve(eq, x)  # ✅ Works for quadratic & cubic
            result = f"Solution: {sol}"
            steps = f"Simplified Equation:<br>\\[{latex(eq)}\\]"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('index.html', result=result, steps=steps)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    message = ''
    filename = ''
    latex_expr = ''
    if request.method == 'POST':
        expr = request.form['expression']
        x = symbols('x')
        try:
            y_expr = sympify(expr)
            latex_expr = latex(y_expr)  # For MathJax rendering

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
    return render_template('graph.html', image=filename, message=message, expression_latex=latex_expr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
