from flask import Flask, render_template, request, jsonify
import pickle
from flask_cors import CORS
import io
from flask import Flask, jsonify, send_file

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dummy user data for login (in a real-world app, use a database)
valid_email = 'test@example.com'
valid_password = 'password123'

# Load the model and vectorizer
with open('mental_health_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Dummy data for doctors
doctors_data = [
    {"id": 1, "name": "Dr. Alice", "specialization": "Psychiatrist"},
    {"id": 2, "name": "Dr. Bob", "specialization": "Therapist"},
    {"id": 3, "name": "Dr. Carol", "specialization": "Neurologist"},
    {"id": 4, "name": "Dr. Dave", "specialization": "Counselor"},
]

# Store booked appointments
appointments = []

# Define recommendations
def provide_recommendations(symptoms):
    transformed_symptoms = vectorizer.transform([symptoms])
    prediction = model.predict(transformed_symptoms)[0]
    recommendations = {
        'Depression': "Primary Treatment: Consider therapy, regular exercise, and maintaining a consistent sleep schedule.\nBooks: 'Feeling Good' by David D. Burns, 'The Noonday Demon' by Andrew Solomon.",
        'Anxiety': "Primary Treatment: Try relaxation techniques like meditation, and seek support from a counselor.\nBooks: 'The Anxiety and Phobia Workbook' by Edmund J. Bourne, 'Dare' by Barry McDonagh.",
        'Bipolar Disorder': "Primary Treatment: Consult a psychiatrist for mood stabilization strategies and medication if needed.\nBooks: 'An Unquiet Mind' by Kay Redfield Jamison, 'The Bipolar Disorder Survival Guide' by David J. Miklowitz.",
        'Cognitive Impairment': "Primary Treatment: Engage in cognitive exercises and consult a neurologist if symptoms persist.\nBooks: 'Keep Sharp' by Sanjay Gupta, 'The Brain's Way of Healing' by Norman Doidge.",
        'Anger Management': "Primary Treatment: Practice mindfulness and consider anger management therapy.\nBooks: 'Anger: Wisdom for Cooling the Flames' by Thich Nhat Hanh, 'The Cow in the Parking Lot' by Leonard Scheff and Susan Edmiston."
    }
    return {
        "condition": prediction,
        "recommendation": recommendations.get(prediction, 'No specific recommendation available.')
    }

# Define the API endpoint for login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check the email and password (this is just an example with static values)
    if email == valid_email and password == valid_password:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 400

# Define the API endpoint for predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'symptoms' not in data:
        return jsonify({"error": "Missing 'symptoms' field in request."}), 400

    symptoms = data['symptoms']
    result = provide_recommendations(symptoms)
    return jsonify(result)

# Define the API endpoint for suggesting doctors
@app.route('/suggest-doctors', methods=['POST'])
def suggest_doctors():
    data = request.json
    symptoms = data.get('symptoms', [])

    # Dummy logic for doctor suggestions based on symptoms
    suggested_doctors = [doctor for doctor in doctors_data if "Psychiatrist" in doctor['specialization'] or "Therapist" in doctor['specialization']]

    return jsonify(suggested_doctors)

# Define the API endpoint for booking appointments
@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time = data.get('time')

    # Find doctor by ID
    doctor = next((doc for doc in doctors_data if doc['id'] == doctor_id), None)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Save appointment details
    appointment = {
        "doctor": doctor,
        "date": date,
        "time": time
    }
    appointments.append(appointment)

    return jsonify({"message": f"Appointment booked with {doctor['name']} on {date} at {time}"}), 200

# Serve the HTML page (index.html)
@app.route('/')
def home():
    return render_template('index.html')

books = [
    {
        "id": 1,
        "title": "Feeling Good",
        "author": "David D. Burns",
        "content": """..."""  # Truncated content from the example above
    },
    {
        "id": 2,
        "title": "The Anxiety and Phobia Workbook",
        "author": "Edmund J. Bourne",
        "content": """..."""  # Truncated content from the example above
    },
    {
        "id": 3,
        "title": "An Unquiet Mind",
        "author": "Kay Redfield Jamison",
        "content": """..."""  # Truncated content from the example above
    }
]

# Route to fetch all books
# @app.route('/books', methods=['GET'])
# def get1_books():
#     return jsonify({"books": books})

# Route to fetch a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Route to download a book's content as a text file
@app.route('/books/<int:book_id>/download', methods=['GET'])
def download_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Create a text file in memory
    content = book['content']
    filename = f"{book['title']}.txt"
    text_file = io.BytesIO()
    text_file.write(content.encode('utf-8'))
    text_file.seek(0)

    return send_file(
        text_file,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )
# @app.route('/books/<int:book_id>/download', methods=['GET'])
# def download_book(book_id):
#     book = next((book for book in books if book['id'] == book_id), None)
#     if book is None:
#         return jsonify({"error": "Book not found"}), 404
    
#     content = f"Title: {book['title']}\nAuthor: {book['author']}\n\n{book['content']}"
#     buffer = io.BytesIO(content.encode('utf-8'))
#     buffer.seek(0)
#     return send_file(
#         buffer,
#         as_attachment=True,
#         download_name=f"{book['title']}.txt",
#         mimetype='text/plain'
#     )



@app.route('/books', methods=['GET'])
def get_books():
    
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
