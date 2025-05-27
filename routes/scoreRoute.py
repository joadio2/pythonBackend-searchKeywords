from fastapi import APIRouter, Request
from sentence_transformers import SentenceTransformer
import json
import re

score = APIRouter()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def create_snippet(text: str, keywords: list[str], window: int = 30) -> str:
    
    lower_text = text.lower()
    keyword_positions = sorted([
        (m.start(), m.end())
        for keyword in keywords
        for m in re.finditer(re.escape(keyword.lower()), lower_text)
    ], key=lambda x: x[0])

    if not keyword_positions:
        return text[:window * 2] + "..." if len(text) > window * 2 else text

    start_pos = max(keyword_positions[0][0] - window, 0)
    end_pos = min(keyword_positions[-1][1] + window, len(text))

    # Avoid cutting words
    while start_pos > 0 and text[start_pos] not in [' ', '.', ',', '\n']:
        start_pos -= 1
    while end_pos < len(text) and text[end_pos] not in [' ', '.', ',', '\n']:
        end_pos += 1

    snippet = text[start_pos:end_pos].strip()

    # Trims multiple spaces and badly cut punctuation
    snippet = re.sub(r'\s+', ' ', snippet)
    snippet = snippet.strip(" .,;:-")

    return snippet + ("..." if end_pos < len(text) else "")

@score.post("/score")
async def score_entries(entries: Request):
    try:
        data = await entries.json()
        if isinstance(data, str):
            data = json.loads(data)

        keyword_texts = [' '.join(entry["matchedKeywords"]) for entry in data]
        texts = [entry["text"] for entry in data]

        embeddings_texts = model.encode(texts, normalize_embeddings=True)
        embeddings_keywords = model.encode(keyword_texts, normalize_embeddings=True)

        scores = (embeddings_texts * embeddings_keywords).sum(axis=1)

        result = []
        for entry, score_val in zip(data, scores):
            snippet = create_snippet(entry["text"], entry["matchedKeywords"], window=30)
            result.append({
                "id": entry["id"],
                "snippet": snippet,
                "keywords": entry["matchedKeywords"],
                "total": len(set(entry["matchedKeywords"])),
                "score": float(score_val)
            })

        result.sort(key=lambda x: x["score"], reverse=True)
        
        return {"results": result}

    except Exception as e:
        print(e)
        return {"error": str(e)}
