# FastAPI Score Service with Sentence Transformers

This is a FastAPI microservice that scores text entries based on their semantic similarity to matched keywords using the [Sentence Transformers](https://www.sbert.net/) model `all-MiniLM-L6-v2`. The service also generates concise text snippets around the matched keywords.

---

## Features

- Scores each text entry by computing similarity between the full text and its matched keywords.
- Extracts a snippet from the text around the keywords for better context visualization.
- Returns results sorted by the semantic similarity score in descending order.

---

## Requirements

- Python 3.8 or higher
- FastAPI
- `sentence-transformers`
- `uvicorn` (for running the server)

---

## Installation

1. Clone the repository (if applicable) or copy the files to your local machine.

2. Create and activate a virtual environment (recommended):

```bash
python -m venv env
source env/bin/activate
```

## Install required Python packages:

pip install fastapi uvicorn
pip install -U sentence-transformers

## Alternatively, if you have a requirements.txt, install dependencies with:

pip install -r requirements.txt

# Usage

Run the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

(Replace main with the name of your Python file without .py)

The scoring endpoint is available at:
POST /score
Request format
Send a JSON array of entries, each with:

id: unique identifier (string or number)
text: full text to analyze (string)
matchedKeywords: list of keywords matched in the text (array of strings)
Example request body:

```json
[
  {
    "id": "1",
    "text": "This is a sample sentence containing keyword1 and keyword2.",
    "matchedKeywords": ["keyword1", "keyword2"]
  },
  {
    "id": "2",
    "text": "Another example text with different keywords.",
    "matchedKeywords": ["example", "keywords"]
  }
]
```

## Response format

The response contains a JSON object with a results array sorted by descending similarity score. Each result contains:

id: the entry id
snippet: a text snippet around the matched keywords
keywords: the matched keywords
total: count of unique matched keywords
score: similarity score (float)
Example response:

```json
{
  "results": [
    {
      "id": "1",
      "snippet": "sample sentence containing keyword1 and keyword2",
      "keywords": ["keyword1", "keyword2"],
      "total": 2,
      "score": 1.2345
    },
    {
      "id": "2",
      "snippet": "example text with different keywords",
      "keywords": ["example", "keywords"],
      "total": 2,
      "score": 0.9876
    }
  ]
}
```

## Code overview

create_snippet(text, keywords, window=30): Extracts a snippet of the text around the keywords with some padding.
POST /score: Endpoint that receives the entries, computes embeddings, calculates similarity scores, and returns sorted results.
Notes

Make sure you have internet access the first time you run the code so the model downloads properly.
The sentence-transformers library version should be updated regularly with pip install -U sentence-transformers to benefit from improvements.
Contact

For questions or support, contact Mauricio Joaquin Dionicio Ali at joaquin.dionicioo@gmail.com.
