from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    a = 'message'
    return render_template('index.html', a=a)

@app.route("/jsonPage1")
def jsonMethod1():
    return render_template('jsonPage.html')
@app.route("/jsonPage2", methods=['POST'])
def jsonMethod2():
    data = request.get_json()
    mail = data['one']
    number = data['two']
    list_one = [mail, number]
    # success callback 함수로 전달
    return jsonify({'mail':mail, 'number':number})

if __name__ == '__main__':
    app.run()