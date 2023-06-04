import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
import flair
from flair.models import TextClassifier
from flair.data import Sentence
import io

# Initialize the Flair sentiment classifier
flair_sentiment_model = TextClassifier.load('en-sentiment')

# Create a function to perform sentiment analysis on the given text
def analyze_sentiment():
    # Get the text from the text box
    text = text_box.get("1.0", "end-1c")

    # Initialize the sentiment scores
    sentiment_scores = {
        'POSITIVE': 0,
        'NEGATIVE': 0,
        'NEUTRAL': 0
    }

    # Analyze the sentiment of each sentence in the text
    sentences = flair.models.SequenceTagger.predict_split_on_whitespace(text, model=flair_sentiment_model)
    for sentence in sentences:
        if sentence.labels[0].value == 'POSITIVE':
            sentiment_scores['POSITIVE'] += sentence.labels[0].score
        elif sentence.labels[0].value == 'NEGATIVE':
            sentiment_scores['NEGATIVE'] += sentence.labels[0].score
        else:
            sentiment_scores['NEUTRAL'] += sentence.labels[0].score

    # Calculate the percentage of each sentiment type
    total_score = sum(sentiment_scores.values())
    sentiment_percentages = {key: value / total_score for key, value in sentiment_scores.items()}

    # Update the labels with the sentiment scores and percentages
    positive_label.config(text="Positive: {:.1%}".format(sentiment_percentages["POSITIVE"]))
    negative_label.config(text="Negative: {:.1%}".format(sentiment_percentages["NEGATIVE"]))
    neutral_label.config(text="Neutral: {:.1%}".format(sentiment_percentages["NEUTRAL"]))

    # Create a pie chart to visualize the sentiment percentages
    fig = plt.figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    colors = ['green', 'red', 'grey']
    labels = list(sentiment_percentages.keys())
    sizes = list(sentiment_percentages.values())
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title("Sentiment Analysis Results")
    plt.show()

    # Highlight the text based on the sentiment scores
    for sentence in sentences:
        if sentence.labels[0].value == 'POSITIVE':
            text_box.tag_add("positive", "1.0+{}c".format(text.index(str(sentence))), "1.0+{}c".format(text.index(str(sentence))+len(str(sentence))))
        elif sentence.labels[0].value == 'NEGATIVE':
            text_box.tag_add("negative", "1.0+{}c".format(text.index(str(sentence))), "1.0+{}c".format(text.index(str(sentence))+len(str(sentence))))
        else:
            text_box.tag_add("neutral", "1.0+{}c".format(text.index(str(sentence))), "1.0+{}c".format(text.index(str(sentence))+len(str(sentence))))

# Create the main window
root = tk.Tk()
root.title("Text Sentiment Analysis")

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=lambda: open_file())
file_menu.add_command(label="Save As", command=lambda: save_file())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=lambda: exit())
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: text_box.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: text_box.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: text_box.event_generate("<<Paste>>"))
analyze_button = tk.Button(root, text="Analyze", command=analyze_sentiment)
analyze_button.pack(side=tk.BOTTOM, padx=5, pady=5)
text_box = tk.Text(root)
text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
positive_label = tk.Label(root, text="Positive: 0%", fg="green")
positive_label.pack(side=tk.LEFT, padx=5, pady=5)
negative_label = tk.Label(root, text="Negative: 0%", fg="red")
negative_label.pack(side=tk.LEFT, padx=5, pady=5)
neutral_label = tk.Label(root, text="Neutral: 0%", fg="grey")
neutral_label.pack(side=tk.LEFT, padx=5, pady=5)
text_box.tag_configure("positive", background="green")
text_box.tag_configure("negative", background="red")
text_box.tag_configure("neutral", background="grey")
# Define the open_file function
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                text_box.delete("1.0", tk.END)
                text_box.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Define the save_file function
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text = text_box.get("1.0", tk.END)
                file.write(text)
        except Exception as e:
            messagebox.showerror("Error", str(e))
root.mainloop()