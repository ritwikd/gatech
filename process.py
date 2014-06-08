from flask import Flask
app = Flask(__name__)

@app.route('/<access_token>')
def hello_world(access_token):
    return access_token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)