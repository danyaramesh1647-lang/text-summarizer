# 📝 Text Summarizer

A Flask web app that shortens long text into a few key sentences using **extractive NLP summarization** with NLTK. No external AI API is used, so the whole pipeline runs on the server and is easy to explain.

## Features

- Large text input with live word, sentence and character count
- Short, medium and long summary modes
- Selected sentences are highlighted in the original text
- Word count reduction and top keywords
- Copy summary and Clear buttons
- Input validation and error messages
- Responsive layout with light and dark mode

## How it works

```
Long Text
   ↓
Preprocessing (sentence split, lowercase, remove stop words)
   ↓
Word frequency scoring
   ↓
Sentence scoring (average word weight, first sentence bonus)
   ↓
Top sentences selected, kept in original order
   ↓
Short Summary
```

1. The text is split into sentences with NLTK `sent_tokenize`.
2. Words are lowercased and stop words are removed.
3. Each word gets a weight based on its frequency (normalised by the most frequent word).
4. Each sentence is scored by the average weight of its words.
5. The top sentences are selected (20%, 35% or 50% of the text for short, medium and long) and put back in their original order.

## Example

**Input**
> Artificial intelligence is transforming many industries. It is being used in healthcare to assist doctors, in education to personalize learning, and in transportation to improve safety. Businesses are also using AI to automate repetitive tasks and analyze large amounts of data.

**Output (short)**
> Artificial intelligence is transforming many industries.

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| NLP | NLTK |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render, Gunicorn |

## Project structure

```
Text-Summarizer/
│
├── app.py                 # Flask routes
├── summarizer.py          # NLTK extractive summarization
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

## Run locally

```bash
git clone https://github.com/danyaramesh1647-lang/text-summarizer.git
cd text-summarizer
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5050. NLTK downloads the data it needs (punkt and stopwords) automatically on the first run.

## API

**POST** `/summarize`

```json
{ "text": "Your long text here...", "length": "medium" }
```

`length` can be `short`, `medium` or `long`. The response contains the summary, the selected sentence indexes, top keywords and word statistics.

## Deploy on Render

1. Push the project to GitHub.
2. Create a new **Web Service** on Render and connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`

## Limitations

- Extractive: it selects existing sentences and does not rewrite them, so the output can be less fluent than an AI-generated summary.
- English text only.
- Works best on articles and essays with at least 5 to 6 sentences.

## Future improvements

- TextRank / TF-IDF scoring
- PDF and URL input
- Abstractive summarization with a transformer model

## Author

**Danya R**
GitHub: [danyaramesh1647-lang](https://github.com/danyaramesh1647-lang)