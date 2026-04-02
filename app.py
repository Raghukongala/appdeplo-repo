from flask import Flask, request, jsonify

app = Flask(__name__)

APP_INFO = {
    "name": "TCS Calculator",
    "company": "Tata Consultancy Services",
    "version": "2.0",
    "description": "A simple calculator API built by TCS"
}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')
    op = data.get('operator')

    if None in (a, b, op):
        return jsonify({'error': 'Missing fields: a, b, operator'}), 400

    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b
    elif op == '%':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a % b
    else:
        return jsonify({'error': f'Unsupported operator: {op}'}), 400

    return jsonify({'result': result, 'powered_by': APP_INFO['company']})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': f"Welcome to {APP_INFO['name']}",
        'company': APP_INFO['company'],
        'version': APP_INFO['version'],
        'description': APP_INFO['description']
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'app': APP_INFO['name'], 'company': APP_INFO['company']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
