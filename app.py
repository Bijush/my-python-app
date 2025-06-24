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

            sol = solve(eq, x)
            if sol:
                result = "Solution: " + ", ".join([f"x = {s}" for s in sol])
            else:
                result = "No real solution found."
            steps = f"Simplified Equation:<br>\\[{latex(eq)}\\]"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('index.html', result=result, steps=steps)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    message = ''
    filename = ''
    latex_expr = ''
    roots = []

    if request.method == 'POST':
        expr = request.form['expression']
        x = symbols('x')
        try:
            y_expr = sympify(expr)
            latex_expr = latex(y_expr)

            f = lambda val: float(y_expr.evalf(subs={x: val}))
            x_vals = np.linspace(-10, 10, 400)
            y_vals = [f(val) for val in x_vals]

            eq = Eq(y_expr, 0)
            roots = solve(eq, x)

            plt.clf()
            plt.figure(figsize=(8, 5))
            plt.plot(x_vals, y_vals, label=f"$y = {latex_expr}$")
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Graph of the Expression')
            plt.grid(True)

            for r in roots:
                if r.is_real:
                    plt.plot(float(r), 0, 'ro')  # Red dot on real root

            plt.legend()
            filename = 'static/graph.png'
            os.makedirs('static', exist_ok=True)
            plt.savefig(filename)
            plt.close()

        except Exception as e:
            message = f"Graph Error: {str(e)}"

    root_str = ", ".join([f"x = {r}" for r in roots]) if roots else "No real roots found"

    return render_template('graph.html',
                           image=filename,
                           message=message,
                           expression_latex=latex_expr,
                           roots=root_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
