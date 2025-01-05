from flask import Flask, render_template

app = Flask(__name__)

# 定义路由
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)