import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Step 1: Create the dataset
data = {
    'symptoms': [
        'fatigue, sleep problems, sadness',  # Depression
        'panic, shortness of breath, worry',  # Anxiety
        'mood swings, irritability, energy',  # Bipolar Disorder
        'tiredness, insomnia, sadness',  # Depression
        'chest pain, anxiety, worry',  # Anxiety
        'feeling hopeless, loss of interest',  # Depression
        'constant worry, irritability, insomnia',  # Anxiety
        'extreme mood swings, irritability, high energy',  # Bipolar Disorder
        'confusion, anger, lack of focus',  # Cognitive Impairment
        'lack of concentration, memory loss, confusion',  # Cognitive Impairment
        'feeling restless, trouble relaxing, constant worry',  # Anxiety
        'irritability, anger, sudden outbursts',  # Anger Management
        'inability to focus, feeling overwhelmed, exhaustion',  # Depression
        'disorientation, forgetfulness, confusion',  # Cognitive Impairment
        'difficulty with memory, feeling lost, confusion',  # Cognitive Impairment
        'feeling trapped, excessive worry, fatigue',  # Anxiety
        'nervousness, constant fear, tension',  # Anxiety
        'low energy, lack of interest, irritability',  # Depression
        'difficulty making decisions, feeling helpless',  # Depression
        'mood swings, impulsivity, euphoria',  # Bipolar Disorder
        'paranoia, excessive worry, nervousness',  # Anxiety
        'feeling numb, emotional detachment',  # Depression
        'difficulty relaxing, excessive thinking, overanalyzing'  # Anxiety
    ],
    'condition': [
        'Depression',
        'Anxiety',
        'Bipolar Disorder',
        'Depression',
        'Anxiety',
        'Depression',
        'Anxiety',
        'Bipolar Disorder',
        'Cognitive Impairment',
        'Cognitive Impairment',
        'Anxiety',
        'Anger Management',
        'Depression',
        'Cognitive Impairment',
        'Cognitive Impairment',
        'Anxiety',
        'Anxiety',
        'Depression',
        'Depression',
        'Bipolar Disorder',
        'Anxiety',
        'Depression',
        'Anxiety'
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Step 2: Preprocess text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['symptoms'])
y = df['condition']

# Step 3: Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train a Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
with open('mental_health_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Step 6: Provide recommendations
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
    return f"Condition: {prediction}.Recommendation: {recommendations.get(prediction, 'No specific recommendation available.')}"

# Test the recommendation system
sample_input = 'difficulty with memory, feeling lost, confusion'
recommendation = provide_recommendations(sample_input)
print("\nSample Input:", sample_input)
print("Recommendation:", recommendation)
