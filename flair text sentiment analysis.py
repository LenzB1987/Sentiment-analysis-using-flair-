import tkinter as tk
from tkinter import ttk
import flair
from flair.data import Sentence

# Initialize Flair sentiment classifier
sentiment_classifier = flair.models.TextClassifier.load('en-sentiment')

# Initialize tkinter window
root = tk.Tk()
root.title("Text Sentiment Analysis")

# Function to analyze text sentiment and update labels
def analyze_text():
    # Get input text from textbox
    input_text = input_box.get("1.0", "end-1c")

    # Create Flair Sentence object
    sentence = Sentence(input_text)

    # Predict sentiment score and label with Flair classifier
    sentiment_classifier.predict(sentence)
    sentiment_score = sentence.labels[0].score
    sentiment_label = sentence.labels[0].value

    # Calculate sentiment percentage and display in label
    sentiment_percentage = sentiment_score * 100
    sentiment_percent_label.config(text=f"{sentiment_percentage:.2f}%")

    # Set label text based on sentiment label and highlight color
    if sentiment_label == 'POSITIVE':
        sentiment_text_label.config(text="Positive")
        sentiment_text_label.config(bg="green")
        sentiment_percent_label.config(fg="green")
    elif sentiment_label == 'NEGATIVE':
        sentiment_text_label.config(text="Negative")
        sentiment_text_label.config(bg="red")
        sentiment_percent_label.config(fg="red")
    else:
        sentiment_text_label.config(text="Neutral")
        sentiment_text_label.config(bg="gray")
        sentiment_percent_label.config(fg="black")

# Create input text box
input_box = tk.Text(root, height=10, width=50)
input_box.pack(pady=10)

# Create analyze button
analyze_button = ttk.Button(root, text="Analyze", command=analyze_text)
analyze_button.pack()

# Create sentiment text label
sentiment_text_label = tk.Label(root, text="", font=("Arial Bold", 14), pady=10)
sentiment_text_label.pack()

# Create sentiment percentage label
sentiment_percent_label = tk.Label(root, text="", font=("Arial", 12), pady=10)
sentiment_percent_label.pack()

root.mainloop()