import tkinter as tk
from tkinter import ttk
import flair
from flair.data import Sentence
from flair.models import TextClassifier

# Initialize Flair sentiment classifier
sentiment_classifier = TextClassifier.load('en-sentiment')

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

    # Get sentiment score and label for each token
    sentiment_spans = sentence.get_spans('sentiment')

    # Set label text based on sentiment label and highlight color for each token
    for span in sentiment_spans:
        sentiment_score = span.score
        sentiment_label = span.value

        # Calculate sentiment percentage and display in label
        sentiment_percentage = sentiment_score * 100

        # Add highlight color to token
        token_index = span.start_pos
        input_box.tag_add(sentiment_label, f"1.{token_index}", f"1.{token_index+len(span.text)}")

        # Add sentiment percentage to tooltip
        input_box.tag_bind(sentiment_label, "<Enter>", lambda event, label=sentiment_label, score=sentiment_percentage: tooltip_label.config(text=f"{label}: {score:.2f}%"))
        input_box.tag_bind(sentiment_label, "<Leave>", lambda event: tooltip_label.config(text=""))

    # Update sentiment percentages for each sentiment label
    positive_percent = sum([span.score for span in sentiment_spans if span.value == 'POSITIVE']) * 100
    negative_percent = sum([span.score for span in sentiment_spans if span.value == 'NEGATIVE']) * 100
    neutral_percent = sum([span.score for span in sentiment_spans if span.value == 'NEUTRAL']) * 100

    # Display sentiment percentages in labels
    positive_percent_label.config(text=f"Positive: {positive_percent:.2f}%")
    negative_percent_label.config(text=f"Negative: {negative_percent:.2f}%")
    neutral_percent_label.config(text=f"Neutral: {neutral_percent:.2f}%")

# Create input text box
input_box = tk.Text(root, height=10, width=50)
input_box.pack(pady=10)

# Create analyze button
analyze_button = ttk.Button(root, text="Analyze", command=analyze_text)
analyze_button.pack()

# Create tooltip label
tooltip_label = tk.Label(root, text="", font=("Arial", 10))
tooltip_label.pack()

# Create sentiment percentage labels
positive_percent_label = tk.Label(root, text="", font=("Arial", 12), pady=5)
positive_percent_label.pack()
negative_percent_label = tk.Label(root, text="", font=("Arial", 12), pady=5)
negative_percent_label.pack()
neutral_percent_label = tk.Label(root, text="", font=("Arial", 12), pady=5)
neutral_percent_label.pack()

# Add sentiment highlight tags and colors
input_box.tag_configure('POSITIVE', background='green')
input_box.tag_configure('NEGATIVE', background='red')
input_box.tag_configure('NEUTRAL', background='gray')

root.mainloop()