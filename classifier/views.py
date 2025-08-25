from django.shortcuts import render
import pickle, re, nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

def home(request):
    return render(request, "classifier/home.html")

def check(request):
    result = None
    if request.method == "POST":
        msg = request.POST.get("message")
        cleaned = clean_text(msg)
        vectorized = vectorizer.transform([cleaned])
        pred = model.predict(vectorized)[0]
        result = "🚨 SPAM" if pred==1 else "✅ HAM (Not Spam)"
    return render(request, "classifier/check.html", {"result": result})

def about(request):
    return render(request, "classifier/about.html")
