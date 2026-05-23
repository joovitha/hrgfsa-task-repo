from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        except Exception as e:
            result = f"Error: {e}"

    return f"""
    <html>
      <head><title>Joovitha task Calculator</title></head>
      <body style="text-align:center; font-family:sans-serif;">
        <h1>Hello from Joovitha. This is my sample Kubernetes project for HRGFSA</h1>
        <h2>Here is Calculator service</h2>
        <form method="post">
          <input type="text" name="num1" placeholder="Enter first number" required>
          <input type="text" name="num2" placeholder="Enter second number" required>
          <select name="operation">
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
            <option value="divide">Divide</option>
          </select>
          <button type="submit">Calculate</button>
        </form>
        <h3>Result: {result if result is not None else ""}</h3>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
