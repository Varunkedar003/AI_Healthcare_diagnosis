import random
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# ===================== BASE DATA =====================

disease_symptoms = {

    "Depression": [
        ["persistent sadness", "loss of interest", "extreme fatigue", "no motivation"],
        ["hopelessness", "low energy", "sleep disturbance", "isolation"],
        ["crying", "worthlessness", "tiredness", "lack of focus"],
        ["sad mood", "appetite loss", "fatigue", "no interest"]
    ],

    "Anxiety": [
        ["excessive worry", "panic", "fast heartbeat", "restlessness"],
        ["nervousness", "sweating", "fear", "tension"],
        ["overthinking", "sleep disturbance", "uneasiness", "stress"],
        ["panic attack", "breathlessness", "fear", "anxiety"]
    ],

    "Bipolar Disorder": [
        ["extreme mood swings", "mania", "depression", "high energy"],
        ["impulsive behavior", "emotional highs", "low mood", "energy bursts"],
        ["risky behavior", "unstable mood", "sudden happiness", "sadness"],
        ["mania phase", "depression phase", "instability", "impulsiveness"]
    ],

    "Cognitive Impairment": [
        ["memory loss", "confusion", "forgetfulness", "difficulty thinking"],
        ["disorientation", "focus issues", "memory decline", "recall problems"],
        ["slow thinking", "forgetting tasks", "confusion", "memory issues"],
        ["difficulty recalling", "mental confusion", "memory problems", "slow thinking"]
    ],

    "Anger Management": [
        ["frequent anger", "irritation", "loss of control", "frustration"],
        ["aggressive behavior", "shouting", "temper issues", "rage"],
        ["emotional outbursts", "anger issues", "stress", "irritability"],
        ["quick temper", "anger", "frustration", "aggression"]
    ],

    "Flu": [
        ["high fever", "chills", "severe body ache", "fatigue"],
        ["fever", "cough", "weakness", "muscle pain"],
        ["sore throat", "fever", "body pain", "chills"],
        ["sweating", "high temperature", "tiredness", "weakness"]
    ],

    "Common Cold": [
        ["runny nose", "sneezing", "nasal congestion", "mild cough"],
        ["blocked nose", "watery eyes", "cold", "fatigue"],
        ["sneezing", "mild fever", "cough", "runny nose"],
        ["nasal congestion", "sore throat", "cold", "fatigue"]
    ],

    "Diabetes": [
        ["frequent urination", "increased thirst", "fatigue", "dry mouth"],
        ["weight loss", "blurred vision", "excessive hunger", "tiredness"],
        ["slow healing wounds", "fatigue", "thirst", "urination"],
        ["high sugar", "fatigue", "thirst", "frequent urination"]
    ],

    "Heart Disease": [
        ["chest pain", "shortness of breath", "fatigue", "pressure"],
        ["tight chest", "sweating", "dizziness", "breathlessness"],
        ["chest discomfort", "pressure", "fatigue", "pain"],
        ["irregular heartbeat", "chest pain", "fatigue", "shortness of breath"]
    ],

    "Migraine": [
        ["severe headache", "nausea", "light sensitivity", "vomiting"],
        ["throbbing headache", "sound sensitivity", "nausea", "dizziness"],
        ["intense headache", "blurred vision", "nausea", "light intolerance"],
        ["headache", "vomiting", "light sensitivity", "pain"]
    ],

    "Arthritis": [
        ["joint pain", "swelling", "stiffness", "inflammation"],
        ["morning stiffness", "joint swelling", "pain", "limited movement"],
        ["joint inflammation", "pain", "reduced mobility", "stiffness"],
        ["pain in joints", "swelling", "stiffness", "movement difficulty"]
    ],

    "Thyroid": [
        ["fatigue", "weight gain", "cold sensitivity", "dry skin"],
        ["hair loss", "tiredness", "low energy", "slow metabolism"],
        ["weight changes", "fatigue", "swelling", "cold feeling"],
        ["low energy", "fatigue", "weight gain", "hormonal imbalance"]
    ],

    "Hypertension": [
        ["high blood pressure", "severe headache", "dizziness", "fatigue"],
        ["blurred vision", "pressure in head", "fatigue", "headache"],
        ["nosebleeds", "high blood pressure", "headache", "dizziness"],
        ["bp high", "headache", "fatigue", "pressure"]
    ],

    "Food Poisoning": [
        ["stomach pain", "vomiting", "diarrhea", "dehydration"],
        ["nausea", "loose motion", "abdominal cramps", "vomiting"],
        ["food infection", "diarrhea", "nausea", "stomach cramps"],
        ["vomiting", "diarrhea", "pain", "weakness"]
    ],

    "Allergy": [
        ["skin rash", "itching", "redness", "swelling"],
        ["sneezing", "watery eyes", "itching", "allergic reaction"],
        ["skin irritation", "rash", "itching", "redness"],
        ["allergy reaction", "itching", "rash", "swelling"]
    ]
}

# ===================== DATA GENERATION =====================

def generate_dataset(samples_per_disease=60):
    symptoms_list = []
    condition_list = []

    noise_words = ["severe", "mild", "persistent", "sudden"]

    for disease, symptom_sets in disease_symptoms.items():
        for _ in range(samples_per_disease):
            combo = random.choice(symptom_sets).copy()
            random.shuffle(combo)

            text = " ".join(combo)

            # add strong variation
            text += " " + random.choice(noise_words)

            symptoms_list.append(text)
            condition_list.append(disease)

    return pd.DataFrame({
        "symptoms": symptoms_list,
        "condition": condition_list
    })

# ===================== CREATE DATA =====================

df = generate_dataset()

df['symptoms'] = df['symptoms'].str.lower()
df = df.sample(frac=1, random_state=42)

print("Dataset size:", len(df))

# ===================== TF-IDF =====================

vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
X = vectorizer.fit_transform(df['symptoms'])
y = df['condition']

# ===================== SPLIT =====================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===================== MODEL =====================

model = MultinomialNB()
model.fit(X_train, y_train)

# ===================== SAVE =====================

with open('mental_health_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("\nModel trained successfully 🚀")

# ===================== TEST =====================

def normalize(text):
    text = text.lower()
    text = text.replace("bp", "blood pressure")
    text = text.replace("tight chest", "chest pain")
    text = text.replace("chest discomfort", "chest pain")
    return text

def test_prediction(text):
    text = normalize(text)

    vec = vectorizer.transform([text])

    probs = model.predict_proba(vec)[0]
    classes = model.classes_

    top3 = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]

    print(f"\nInput: {text}")
    for disease, prob in top3:
        print(f"{disease} → {round(prob*100,2)}%")

# test
test_prediction("tight chest discomfort sweating dizziness")
test_prediction("sad low energy hopeless")
test_prediction("fever cough body pain")