import re

INTENTS = [
    {
        'name': 'greeting',
        'patterns': [re.compile(r'^(hi|hello|hey|good\s(morning|afternoon|evening))\b', re.I)],
        'keywords': {
            'hello': 3, 'hi': 3, 'hey': 3, 'greetings': 3,
            'good morning': 3, 'good afternoon': 3, 'good evening': 3,
        },
    },
    {
        'name': 'farewell',
        'patterns': [],
        'keywords': {'bye': 3, 'goodbye': 3, 'farewell': 3, 'see you': 2, 'take care': 2, 'good night': 2},
    },
    {
        'name': 'thanks',
        'patterns': [re.compile(r'\b(very|really|so|quite)\s+helpful\b', re.I)],
        'keywords': {'thank': 3, 'thanks': 3, 'thank you': 3, 'appreciate': 2, 'helpful': 2},
    },
    {
        'name': 'help',
        'patterns': [re.compile(r'what can you (do|help)', re.I), re.compile(r'what do you do', re.I)],
        'keywords': {'help': 3, 'assist': 3, 'support': 2, 'option': 2, 'service': 2, 'menu': 2},
    },
    {
        'name': 'admission',
        'patterns': [],
        'keywords': {
            'admission': 5, 'admissions': 5, 'apply': 4, 'application': 5,
            'enroll': 4, 'enrollment': 4, 'new student': 5, 'intake': 4,
            'requirement': 3, 'qualify': 3, 'eligible': 3, 'acceptance': 4,
            'jamb': 5, 'post utme': 5, 'post-utme': 5, 'screening': 4,
            'admission form': 5, 'gain admission': 5,
            'cutoff': 5, 'cut off': 5, 'cutoff mark': 5, 'cut off mark': 5,
            'minimum score': 5, 'jamb score': 5, 'jamb cutoff': 5,
        },
    },
    {
        'name': 'courses',
        'patterns': [],
        'keywords': {
            'course': 4, 'courses': 4, 'subject': 3, 'module': 4,
            'unit': 3, 'class': 3, 'lecture': 3, 'credit': 3,
            'programme': 4, 'program': 4, 'department': 3, 'faculty': 3,
            'faculties': 4, 'curriculum': 4, 'add course': 5, 'drop course': 5,
            'course registration': 5, 'what courses': 4, 'available courses': 4,
            'jamb subjects': 5, 'jamb subject': 5,
        },
    },
    {
        'name': 'fees',
        'patterns': [],
        'keywords': {
            'fee': 5, 'fees': 5, 'tuition': 5, 'payment': 4, 'pay': 3,
            'charges': 4, 'cost': 3, 'how much': 4, 'bursary': 4,
            'school fee': 5, 'acceptance fee': 5, 'fee payment': 5, 'remita': 4,
        },
    },
    {
        'name': 'exam',
        'patterns': [],
        'keywords': {
            'exam': 5, 'exams': 5, 'examination': 5, 'test': 3,
            'timetable': 4, 'schedule': 3, 'venue': 3,
            'resit': 5, 'carryover': 5, 'carry over': 5,
            'supplementary': 4, 'exam date': 5, 'exam rules': 4, 'malpractice': 4,
        },
    },
    {
        'name': 'results',
        'patterns': [],
        'keywords': {
            'result': 5, 'results': 5, 'grade': 5, 'grades': 5,
            'score': 4, 'marks': 4, 'cgpa': 5, 'gpa': 5,
            'transcript': 5, 'fail': 3, 'pass': 3, 'check result': 5,
            'academic standing': 4, 'probation': 4,
        },
    },
    {
        'name': 'hostel',
        'patterns': [],
        'keywords': {
            'hostel': 5, 'hostels': 5, 'accommodation': 5, 'room': 3,
            'dormitory': 5, 'lodge': 3, 'bedspace': 5,
            'on campus': 4, 'hall of residence': 5, 'live on campus': 4,
        },
    },
    {
        'name': 'library',
        'patterns': [],
        'keywords': {
            'library': 5, 'book': 4, 'books': 4, 'borrow': 4, 'return': 3,
            'resource': 3, 'journal': 4, 'study room': 4,
            'digital library': 5, 'e-library': 5, 'elibrary': 5,
            'library hours': 5, 'library fine': 5,
        },
    },
    {
        'name': 'calendar',
        'patterns': [re.compile(r'harmattan.{0,20}(exam|timetable)', re.I)],
        'keywords': {
            'calendar': 4, 'academic calendar': 5, 'semester': 4,
            'holiday': 4, 'vacation': 4, 'resumption': 5,
            'harmattan': 5, 'rain semester': 5, 'school start': 4, 'semester start': 5,
        },
    },
    {
        'name': 'contact',
        'patterns': [],
        'keywords': {
            'contact': 6, 'phone': 4, 'email': 4, 'address': 3,
            'staff': 3, 'office': 3, 'number': 3, 'reach': 3,
            'registrar': 5, 'hod': 4, 'dean': 4,
            'vice chancellor': 4, 'student affairs': 5, 'ict': 3,
        },
    },
    {
        'name': 'scholarship',
        'patterns': [],
        'keywords': {
            'scholarship': 5, 'scholarships': 5, 'financial aid': 5,
            'grant': 4, 'award': 3, 'sponsorship': 4, 'loan': 4,
            'waiver': 4, 'bursary': 4, 'state bursary': 5,
            'government scholarship': 5, 'merit scholarship': 5,
            'nddc': 5, 'ptdf': 5, 'fgsb': 5, 'shell scholarship': 5,
            'agip': 4, 'federal scholarship': 5, 'niger delta': 4,
            'petroleum fund': 4, 'free education': 3,
        },
    },
]
