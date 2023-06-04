import tkinter as tk
from tkinter import scrolledtext, messagebox
import matplotlib.pyplot as plt
from flair.models import TextClassifier
from flair.data import Sentence

# Initialize the sentiment classifier
classifier = TextClassifier.load("en-sentiment")

# Define a function to analyze the sentiment of the text
def analyze_sentiment():
    # Get the text from the text box
    text = text_box.get("1.0", "end-1c")
    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text to analyze.")
        return
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
    # Set the color of the result text box based on the level of sentiment
    if label == "NEGATIVE":
        result_box.configure(bg="#ff9999", fg="#000000")
    elif label == "POSITIVE":
        result_box.configure(bg="#99ff99", fg="#000000")
    else:
        result_box.configure(bg="#ffff99", fg="#000000")
    # Update the sentiment percentages
    sentiment_counts[label] += 1
    total_counts = sum(sentiment_counts.values())
    for label, count in sentiment_counts.items():
        percentages[label] = count / total_counts * 100
    # Update the pie chart
    plot_sentiment()

# Define a function to plot the sentiment percentages in a pie chart
def plot_sentiment():
    # Create a pie chart of the sentiment percentages
    fig, ax = plt.subplots()
    ax.pie(percentages.values(), labels=percentages.keys(), autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that the pie is drawn as a circle.
    ax.set_title("Sentiment Analysis")
    # Display the pie chart
    plt.show()

# Initialize the sentiment counts and percentages
sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
percentages = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

# Create the GUI window
window = tk.Tk()
window.title("Sentiment Analysis")

# Create the label for the input text box
text_label = tk.Label(window, text="Enter some text to analyze:")
text_label.pack()

# Create the text box for input text
text_box = scrolledtext.ScrolledText(window, width=50, height=10, wrap="word")
text_box.pack()

# Create the analyze button
analyze_button = tk.Button(window, text="Analyze", command=analyze_sentiment)
analyze_button.pack()

# Create the label for the sentiment analysis results text box
result_label = tk.Label(window, text="Sentiment analysis results:")
result_label.pack()

# Create the text box for displaying the sentiment analysis results
result_box = scrolledtext.ScrolledText(window, width=50, height=10, wrap="word", state="disabled")
result_box.pack()

# Create the quit button
quit_button = tk.Button(window, text="Quit", command=window.quit)
quit_button.pack()

# Start the GUI event loop
window.mainloop()