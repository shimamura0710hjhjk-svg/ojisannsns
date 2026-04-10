from flask import Flask, render_template, request, jsonify
from converters import ojisan_converter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    
    results = {}
    
    # おじさんモード
    if 'ojisan_text' in data and data['ojisan_text'].strip():
        results['ojisan'] = ojisan_converter(data['ojisan_text'])
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
