import io
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((350, 350))
        photo = ImageTk.PhotoImage(image)
        canvas.image = photo
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

def analyze_sentiment():
    if canvas.image:
        analyzer = SentimentIntensityAnalyzer()
        image = canvas.image
        buffer = io.BytesIO()
        image.save(buffer, format='jpg')
        image_bytes = buffer.getvalue()

        scores = analyzer.polarity_scores(image_bytes)

        positive_percentage = scores['pos'] * 100
        negative_percentage = scores['neg'] * 100
        neutral_percentage = scores['neu'] * 100

        total = positive_percentage + negative_percentage + neutral_percentage

        if total > 0:
            positive_color = f'#{int(255 * positive_percentage / total):02x}ff{int(255 * (100 - positive_percentage) / total):02x}'
            negative_color = f'#{int(255 * negative_percentage / total):02x}ff{int(255 * (100 - negative_percentage) / total):02x}'
            neutral_color = f'#{int(255 * neutral_percentage / total):02x}ff{int(255 * (100 - neutral_percentage) / total):02x}'

            canvas.create_rectangle(10, 10, 80, 80, fill=positive_color)
            canvas.create_rectangle(100, 10, 170, 80, fill=negative_color)
            canvas.create_rectangle(190, 10, 260, 80, fill=neutral_color)

            canvas.create_text(45, 45, text=f'{positive_percentage:.1f}%', fill='black')
            canvas.create_text(135, 45, text=f'{negative_percentage:.1f}%', fill='black')
            canvas.create_text(225, 45, text=f'{neutral_percentage:.1f}%', fill='black')

root = tk.Tk()
root.title('Image Sentiment Analysis')

canvas = tk.Canvas(root, width=350, height=350)
canvas.pack()

upload_button = tk.Button(root, text='Upload Image', command=open_image)
upload_button.pack()

analyze_button = tk.Button(root, text='Analyze Sentiment', command=analyze_sentiment)
analyze_button.pack()

root.mainloop()