from flask import Flask, render_template, request, jsonify
import requests
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Cipher:riKXPIASClOaF7sm@cluster0.iqltodr.mongodb.net/registrations"
mongodb_client = PyMongo(app)
db = mongodb_client.db
#  mongodb = riKXPIASClOaF7sm
mongo = PyMongo(app)
colab_api_url = "https://a01c-34-147-10-113.ngrok-free.app/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # def translate():
    # data = request.get_json()
    # texts = data.get('texts', [])
    # target_lang = data.get('target_lang', 'en')
    # translated_texts = indic2en_Model.batch_translate(texts, 'en', target_lang)
    # return jsonify({'translated_texts': translated_texts})

    data = request.get_json()
    texts = data.get('texts', [])
    target_lang = data.get('target_lang', 'en')
    print("texts:", texts)
    print("target_lang:", target_lang)
    response = requests.post(f"{colab_api_url}/translate", json={'texts': texts, 'target_lang': target_lang})
    if response.status_code == 200:
        translated_texts = response.json().get('translated_texts', [])
        return jsonify({'translated_texts': translated_texts})
    else:
        return jsonify({'error': 'Failed to get translation'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')

@app.route('/register-data', methods=['POST'])
def register_data():
    try:
        if request.method == 'POST':
            collegeName = request.json.get('collegeName')
            instituteType = request.json.get('instituteType')
            state = request.json.get('state')
            email = request.json.get('email')
            contactNumber = request.json.get('contactNumber')
            collegeAddress = request.json.get('collegeAddress')
            postalCode = request.json.get('postalCode')
            checkbox = request.json.get('checkbox', False)

            db.institutes.insert_one({
                'collegeName': collegeName,
                'instituteType': instituteType,
                'state': state,
                'email': email,
                'contactNumber': contactNumber,
                'collegeAddress': collegeAddress,
                'postalCode': postalCode,
                'checkbox': checkbox,
            })

            return jsonify({'message': 'success'})
        else:
            return jsonify({'error': 'Invalid request method'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)