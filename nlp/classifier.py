from nlp.tokenizer import tokenize
from nlp.intents import INTENTS


def _matches(token: str, keyword: str) -> bool:
    if token == keyword:
        return True
    if len(keyword) >= 4 and token.startswith(keyword):
        return True
    if len(keyword) >= 4 and keyword.startswith(token) and len(token) >= 4:
        return True
    return False


def classify(text: str) -> tuple:
    lower = text.lower().strip()
    tokens = tokenize(text)
    scores = []

    for intent in INTENTS:
        score = 0

        for pattern in intent.get('patterns', []):
            if pattern.search(lower):
                score += 6

        for keyword, weight in intent['keywords'].items():
            if ' ' in keyword:
                if keyword in lower:
                    score += weight
            else:
                for token in tokens:
                    if _matches(token, keyword):
                        score += weight
                        break

        scores.append((intent['name'], score))

    scores.sort(key=lambda x: x[1], reverse=True)
    best_intent, best_score = scores[0]
    second_score = scores[1][1] if len(scores) > 1 else 0
    gap = best_score - second_score
    confidence = min((best_score + gap * 0.5) / 12, 1.0) if best_score > 0 else 0.0

    if best_score >= 2:
        return best_intent, round(confidence, 2)
    return 'unknown', 0.0
