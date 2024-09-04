from flask import Flask, jsonify,request
from resume_checker import evaluate_cv
import os


app = Flask(__name__)

api_key = os.getenv('API_KEY')

@app.route('/')
def hello():
    return "Heellllo!"


@app.route('/evaluateCV', methods=['POST'])
def evaluateCV():

    data = request.json
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    url = data.get('urlCv')
    path = data.get('savePath')
    type=data.get('resumeType')

    if not url or not path:
        return jsonify({'error': 'Please provide all required data'}), 400

    try:
        rating,unmatched=evaluate_cv(url, path,type)
        keywords_list = list(unmatched)
        if rating==-1:       
            return jsonify({'error': 'Invalid pdf url'}), 400
        else:
            return jsonify({'rating':rating,'missing keywords':keywords_list}), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({'message': 'Internal Server Error', 'error': error_message}), 500



if __name__ == '__main__':
    app.run(debug=True)