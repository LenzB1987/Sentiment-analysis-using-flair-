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

    # Loop through words in sentence and add tags
    for token in sentence.tokens:
        # Get sentiment score and label for each word
        sentiment_score = token.get_tag('sentiment').score
        sentiment_label = token.get_tag('sentiment').value

        # Set tag label text based on sentiment label and highlight color
        if sentiment_label == 'POSITIVE':
            tag_label = tk.Label(text=sentiment_label, bg="green", fg="white")
        elif sentiment_label == 'NEGATIVE':
            tag_label = tk.Label(text=sentiment_label, bg="red", fg="white")
        else:
            tag_label = tk.Label(text=sentiment_label, bg="gray", fg="black")
        
        # Add tag to text box
        input_box.tag_add(str(sentiment_score), f"{token.start_pos}", f"{token.end_pos}")
        input_box.tag_config(str(sentiment_score), font=("Arial", 12), underline=1)
        input_box.window_create(f"{token.start_pos}", window=tag_label)

# Create input text box
input_box = tk.Text(root, height=10, width=50)
input_box.pack(pady=10)

# Create analyze button
analyze_button = ttk.Button(root, text="Analyze", command=analyze_text)
analyze_button.pack()

root.mainloop()