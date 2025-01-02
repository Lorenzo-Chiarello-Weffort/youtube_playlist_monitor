from flask import Flask, render_template
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    credentials_str = os.getenv('GOOGLE_OAUTH_CREDENTIALS')

    if credentials_str:
        credentials = json.loads(credentials_str)
        token = credentials.get('token')
        print(f'Token: {token}')
        return render_template('index.html')
    else:
        print("As credenciais não foram encontradas.")
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)