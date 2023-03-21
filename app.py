from flask import Flask,request,render_template
# import pandas as pand

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return """
    <h1>Start Machine Learning Project</h1>
    """




if __name__ == '__main__':
    app.run(debug=True)