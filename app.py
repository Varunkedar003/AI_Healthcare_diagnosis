from flask import Flask, render_template, request, jsonify, send_file
import pickle
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# ===================== LOAD MODEL =====================

with open('mental_health_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# ===================== NORMALIZATION =====================

def normalize(text):
    text = text.lower()
    text = text.replace("bp", "blood pressure")
    text = text.replace("tight chest", "chest pain")
    text = text.replace("chest discomfort", "chest pain")
    text = text.replace("tired", "fatigue")
    text = text.replace("loose motion", "diarrhea")
    return text

# ===================== TEMP USER STORAGE =====================

users = []

# ===================== PAGE ROUTES =====================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/relaxation')
def relaxation():
    return render_template('relaxation.html')

@app.route('/call')
def call():
    return render_template('call.html')

@app.route('/books-page')
def books_page():
    return render_template('books.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# ===================== LOGIN =====================

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    for user in users:
        if user['email'] == data.get('email') and user['password'] == data.get('password'):
            return jsonify({"message": "Login successful!"})

    if data.get('email') == "test@example.com" and data.get('password') == "password123":
        return jsonify({"message": "Login successful!"})

    return jsonify({"error": "Invalid email or password"}), 400

# ===================== REGISTER =====================

@app.route('/register-user', methods=['POST'])
def register_user():
    data = request.json

    users.append({
        "name": data.get('name'),
        "email": data.get('email'),
        "password": data.get('password')
    })

    return jsonify({"message": "Registered successfully"})

# ===================== PREDICTION =====================

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms')

    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    # normalize input
    text = normalize(symptoms)

    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()

    # recommendations
    recommendations = {
        'Depression': "Exercise, therapy, proper sleep",
        'Anxiety': "Meditation and relaxation",
        'Bipolar Disorder': "Consult psychiatrist",
        'Cognitive Impairment': "Brain exercises",
        'Anger Management': "Mindfulness practice",
        'Flu': "Rest and hydration",
        'Common Cold': "Drink fluids",
        'Diabetes': "Monitor sugar levels",
        'Heart Disease': "Seek medical help immediately",
        'Migraine': "Rest in dark room",
        'Arthritis': "Exercise and medication",
        'Thyroid': "Check hormone levels",
        'Hypertension': "Reduce salt intake",
        'Food Poisoning': "Stay hydrated",
        'Allergy': "Avoid allergens"
    }

    return jsonify({
        "condition": prediction,
        "confidence": round(confidence * 100, 2),
        "recommendation": recommendations.get(prediction, "No recommendation available")
    })

# ===================== BOOKS =====================

books = [
    {"id": 1, "title": "Feeling Good", "author": "David Burns", "content": "Sample content"},
    {"id": 2, "title": "Anxiety Workbook", "author": "Edmund Bourne", "content": "Sample content"}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>/download')
def download_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        return jsonify({"error": "Not found"}), 404

    buffer = io.BytesIO(book['content'].encode())

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{book['title']}.txt",
        mimetype='text/plain'
    )

# ===================== RUN =====================

if __name__ == '__main__':
    app.run(debug=True)