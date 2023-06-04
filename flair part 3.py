import tkinter as tk
from tkinter import scrolledtext
from flair.models import TextClassifier
from flair.data import Sentence

# Initialize the sentiment classifier
classifier = TextClassifier.load("en-sentiment")

# Define a function to analyze the sentiment of the text
def analyze_sentiment():
    # Get the text from the text box
    text = text_box.get("1.0", "end-1c")
    # Create a sentence object from the text
    sentence = Sentence(text)
    # Run the sentiment classifier on the sentence
    classifier.predict(sentence)
    # Get the sentiment label and score from the sentence
    label = sentence.labels[0].value
    score = sentence.labels[0].score
    # Display the sentiment analysis results
    result_box.delete("1.0", "end")
    result_box.insert("end", f"Sentiment: {label}\n")
    result_box.insert("end", f"Score: {score:.2f}")

# Create the GUI window
window = tk.Tk()
window.title("Sentiment Analysis")

# Create the text box for input text
text_box = scrolledtext.ScrolledText(window, width=50, height=10)
text_box.pack()

# Create the analyze button
analyze_button = tk.Button(window, text="Analyze", command=analyze_sentiment)
analyze_button.pack()

# Create the text box for displaying the sentiment analysis results
result_box = scrolledtext.ScrolledText(window, width=50, height=10)
result_box.pack()

# Start the GUI event loop
window.mainloop()