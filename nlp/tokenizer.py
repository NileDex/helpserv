import re

STOP_WORDS = {
    'a', 'an', 'the',
    'i', 'me', 'my', 'we', 'our', 'you', 'your',
    'he', 'him', 'his', 'she', 'her', 'it', 'its', 'they', 'them', 'their',
    'and', 'but', 'if', 'or', 'as', 'of', 'at', 'by', 'for', 'with',
    'about', 'into', 'to', 'from', 'in', 'on', 'off', 'over', 'up', 'down',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'can',
    'this', 'that', 'these', 'those',
    'just', 'now', 'very', 'too', 'so', 'not', 'no', 'also',
    'which', 'who', 'whom', 's', 't',
}


def tokenize(text: str) -> list:
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return [t for t in text.split() if len(t) > 1 and t not in STOP_WORDS]
