import re

DEPARTMENTS = [
    # Engineering
    'civil engineering', 'mechanical engineering', 'electrical engineering',
    'electronic engineering', 'chemical engineering', 'petroleum engineering',
    'gas engineering', 'computer engineering', 'marine engineering',
    'agricultural engineering', 'engineering',
    # Sciences
    'computer science', 'microbiology', 'biochemistry', 'geology',
    'mathematics', 'physics', 'chemistry', 'biology', 'statistics',
    'industrial chemistry', 'sciences',
    # Management
    'accounting', 'business administration', 'banking', 'finance',
    'marketing', 'public administration', 'insurance',
    'management sciences', 'management',
    # Humanities & Social Sciences
    'english', 'history', 'philosophy', 'theatre', 'film studies',
    'mass communication', 'political science', 'sociology', 'psychology',
    'french', 'economics', 'humanities', 'social sciences', 'arts',
    # Law
    'law',
    # Medicine
    'medicine', 'surgery', 'anatomy', 'physiology', 'pharmacology',
    'clinical sciences',
    # Pharmacy
    'pharmacy',
    # Agriculture
    'agriculture', 'animal science', 'crop science', 'forestry',
    'agricultural economics',
    # Environmental Sciences
    'architecture', 'urban planning', 'quantity surveying',
    'estate management', 'building technology', 'environmental sciences',
    # Education
    'education', 'guidance', 'counselling', 'curriculum studies',
]

LEVELS = [
    '100 level', '200 level', '300 level', '400 level',
    '500 level', '600 level', '700 level',
]

SEMESTERS = [
    'first semester', 'second semester',
    'harmattan semester', 'rain semester',
    'harmattan', 'rain',
]

SCHOLARSHIPS = [
    'fgsb', 'nddc', 'ptdf', 'shell scholarship', 'agip scholarship',
    'eni scholarship', 'rivers state bursary', 'state bursary',
    'merit scholarship', 'federal scholarship',
]


def extract_entities(text: str) -> dict:
    lower = text.lower()
    entities = {}

    for dept in DEPARTMENTS:
        if dept in lower:
            entities['department'] = dept
            break

    for level in LEVELS:
        if level in lower:
            entities['level'] = level
            break

    for sem in SEMESTERS:
        if sem in lower:
            entities['semester'] = sem
            break

    for schol in SCHOLARSHIPS:
        if schol in lower:
            entities['scholarship'] = schol
            break

    m = re.search(r'\b(20\d{2})\b', text)
    if m:
        entities['year'] = m.group(1)

    m = re.search(r'\b[A-Z]{2,}/\d{4}/\d+\b', text)
    if m:
        entities['matric'] = m.group(0)

    return entities
