import random
from data.knowledge_base import KB

SUGGESTIONS = {
    'greeting':    ['What are the admission requirements?', 'How do I pay my school fees?', 'Tell me about scholarships'],
    'help':        ['Admission requirements', 'How to pay school fees', 'Exam timetable info'],
    'admission':   ['What is the JAMB cutoff mark?', 'What subjects do I need for Engineering?', 'Tell me about Post-UTME'],
    'courses':     ['What JAMB subjects do I need for Medicine?', 'Tell me about Management Science departments', 'How do I register courses?'],
    'fees':        ['What are the Engineering fees?', 'Are there any scholarships?', 'When is the payment deadline?'],
    'exam':        ['What are the grading scores?', 'When are results released?', 'What about carryover exams?'],
    'results':     ['What CGPA do I need for First Class?', 'How do I request a transcript?', 'Tell me about scholarships'],
    'hostel':      ['What are the hostel rules?', 'How much is hostel fee?', 'Tell me about library hours'],
    'library':     ['Can I access e-library from home?', 'What databases are available?', 'What is the borrowing limit?'],
    'calendar':    ['When does harmattan semester start?', 'When are harmattan exams?', 'When does rain semester begin?'],
    'contact':     ['How do I contact the bursary?', 'How do I reach student affairs?', 'Where is the admissions office?'],
    'scholarship': ['What CGPA do I need for scholarship?', 'How do I apply for NDDC scholarship?', 'Tell me about PTDF'],
    'thanks':      ['Anything else I can help with?', 'Tell me about fees', 'Ask me about scholarships'],
    'farewell':    [],
    'unknown':     ['What are the admission requirements?', 'How do I pay school fees?', 'Tell me about scholarships'],
}

_FACULTY_KEYWORDS = {
    'engineering':           'Engineering',
    'civil engineering':     'Engineering',
    'mechanical':            'Engineering',
    'electrical':            'Engineering',
    'chemical engineering':  'Engineering',
    'petroleum':             'Engineering',
    'marine engineering':    'Engineering',
    'computer engineering':  'Engineering',
    'agricultural engineering': 'Engineering',
    'science':               'Science',
    'computer science':      'Science',
    'microbiology':          'Science',
    'biochemistry':          'Science',
    'geology':               'Science',
    'biology':               'Science',
    'chemistry':             'Science',
    'physics':               'Science',
    'mathematics':           'Science',
    'statistics':            'Science',
    'management':            'Management Sciences',
    'management sciences':   'Management Sciences',
    'accounting':            'Management Sciences',
    'banking':               'Management Sciences',
    'finance':               'Management Sciences',
    'marketing':             'Management Sciences',
    'public administration': 'Management Sciences',
    'insurance':             'Management Sciences',
    'law':                   'Law',
    'llb':                   'Law',
    'arts':                  'Humanities & Social Sciences',
    'humanities':            'Humanities & Social Sciences',
    'mass communication':    'Humanities & Social Sciences',
    'sociology':             'Humanities & Social Sciences',
    'psychology':            'Humanities & Social Sciences',
    'political science':     'Humanities & Social Sciences',
    'english':               'Humanities & Social Sciences',
    'history':               'Humanities & Social Sciences',
    'philosophy':            'Humanities & Social Sciences',
    'economics':             'Humanities & Social Sciences',
    'agriculture':           'Agriculture',
    'animal science':        'Agriculture',
    'crop science':          'Agriculture',
    'forestry':              'Agriculture',
    'education':             'Education',
    'guidance':              'Education',
    'counselling':           'Education',
    'architecture':          'Environmental Sciences',
    'urban planning':        'Environmental Sciences',
    'quantity surveying':    'Environmental Sciences',
    'estate management':     'Environmental Sciences',
    'building technology':   'Environmental Sciences',
    'environmental':         'Environmental Sciences',
    'medicine':              'Medicine & Surgery',
    'surgery':               'Medicine & Surgery',
    'mbbs':                  'Medicine & Surgery',
    'pharmacy':              'Pharmacy',
    'b.pharm':               'Pharmacy',
    'anatomy':               'Basic Medical Sciences',
    'physiology':            'Basic Medical Sciences',
    'pharmacology':          'Basic Medical Sciences',
}


def _p(opts): return random.choice(opts)


def _detect_faculty(raw):
    raw = raw.lower()
    for keyword, faculty in _FACULTY_KEYWORDS.items():
        if keyword in raw:
            return faculty
    return None


def _greeting(_e):
    return _p([
        f"Hello! I'm UniHelp, your {KB['university']['name']} student assistant.\n\nHow can I help you today?",
        f"Hi there! Welcome to the {KB['university']['name']} HelpDesk. What do you need help with?",
        "Hey! I can assist with admissions, fees, exams, hostel, library, scholarships, and more. Ask me anything!",
    ])


def _farewell(_e):
    return _p([
        'Goodbye! Have a great day. Feel free to return anytime!',
        'Take care! Best of luck with your studies at RSU.',
        "Bye! I'm available 24/7 for all your Rivers State University queries.",
    ])


def _thanks(_e):
    return _p([
        "You're welcome! Is there anything else I can help you with?",
        "Happy to help! Don't hesitate to ask more questions.",
        'Glad I could assist! Ask me anything else about RSU.',
    ])


def _help(_e):
    return (
        "Here's everything I can help you with at **Rivers State University**:\n\n"
        "• **Admission** – requirements, JAMB cutoff, Post-UTME, application process\n"
        "• **Courses** – faculties, departments, JAMB subjects per course\n"
        "• **Fees** – tuition ranges by faculty, payment methods, deadlines\n"
        "• **Exams** – timetable, rules, grading system, resit/carryover\n"
        "• **Results** – CGPA classification, how to check, transcripts\n"
        "• **Hostel** – accommodation, application, hostel rules\n"
        "• **Library** – hours, borrowing limits, e-library, databases\n"
        "• **Calendar** – harmattan & rain semesters, resumption dates\n"
        "• **Contacts** – offices, emails, phone numbers\n"
        "• **Scholarships** – FGSB, NDDC, PTDF, Rivers State bursary, and more\n\n"
        "Type your question and I'll answer right away!"
    )


def _admission(e):
    a = KB['admission']
    raw = e.get('_raw', '').lower()

    if any(w in raw for w in ['cutoff', 'cut off', 'jamb score', 'minimum score', 'jamb mark', 'jamb cutoff']):
        c = a['jamb_cutoff']
        return (
            f"**JAMB Cutoff Marks – {KB['university']['name']}**\n\n"
            f"• General minimum: **{c['general_minimum']}**\n"
            f"• Medicine & Surgery: **{c['medicine_surgery']}**\n"
            f"• Pharmacy: **{c['pharmacy']}**\n"
            f"• Law: **{c['law']}**\n"
            f"• Engineering: **{c['engineering']}**\n"
            f"• Sciences: **{c['sciences']}**\n"
            f"• Management Sciences: **{c['management_sciences']}**\n"
            f"• Arts & Humanities: **{c['arts_humanities']}**\n"
            f"• Education: **{c['education']}**\n"
            f"• Agriculture: **{c['agriculture']}**\n\n"
            "**Note:** A higher JAMB score significantly improves your chances. "
            "Meeting the cutoff does not guarantee admission - Post-UTME performance also counts.\n\n"
            f"**Post-UTME:** {a['post_utme']}\n\n"
            f"**Contact:** {a['contact']}"
        )

    if 'post utme' in raw or 'post-utme' in raw or 'screening' in raw:
        return (
            f"**RSU Post-UTME Screening**\n\n"
            f"{a['post_utme']}\n\n"
            "**How to Register:**\n"
            f"1. Visit {a['portal']}\n"
            "2. Log in with your JAMB registration number\n"
            "3. Purchase the Post-UTME form\n"
            "4. Schedule your CBT date and centre\n\n"
            f"**Contact:** {a['contact']}"
        )

    reqs  = '\n'.join(f'• {r}' for r in a['requirements'])
    steps = '\n'.join(f'{i+1}. {s}' for i, s in enumerate(a['process']))
    return (
        f"**Admission – {KB['university']['name']}**\n\n"
        f"**Requirements:**\n{reqs}\n\n"
        f"**Application Process:**\n{steps}\n\n"
        f"**Deadline:** {a['deadline']}\n\n"
        f"**Post-UTME:** {a['post_utme']}\n\n"
        f"**Apply here:** {a['portal']}\n"
        f"**Contact:** {a['contact']}"
    )


def _courses(e):
    raw = e.get('_raw', '')
    faculty_name = _detect_faculty(raw)

    if faculty_name:
        f = KB['faculties'].get(faculty_name, {})
        if f:
            depts = '\n'.join(f'• {d}' for d in f.get('departments', []))
            note_line = f"\n**Note:** {f['note']}\n" if 'note' in f else ''
            return (
                f"**{f.get('full_name', faculty_name)}**\n\n"
                f"**Departments / Programmes:**\n{depts}\n\n"
                f"**JAMB Subjects Required:** {f.get('jamb_subjects', 'See RSU website')}\n\n"
                f"**Degree Awarded:** {f.get('degree', 'B.Sc')}  |  "
                f"**Duration:** {f.get('duration', '4 years')}\n"
                f"{note_line}\n"
                f"**Portal:** {KB['university']['ecampus']}\n"
                f"**Registrar:** {KB['contacts']['registrar']}"
            )

    fac_lines = []
    for name, info in KB['faculties'].items():
        sample = ', '.join(info['departments'][:2])
        more = f' + {len(info["departments"]) - 2} more' if len(info['departments']) > 2 else ''
        fac_lines.append(f"• **{name}** - {sample}{more}")
    faculties_list = '\n'.join(fac_lines)

    return (
        f"**Faculties & Programmes – {KB['university']['name']}**\n\n"
        f"{faculties_list}\n\n"
        "**Course Registration:**\n"
        "1. Log in to ecampus.rsu.edu.ng\n"
        "2. Navigate to **Course Registration**\n"
        "3. Select your approved courses and submit before the deadline\n\n"
        "Ask about a specific faculty to get its departments and JAMB subject requirements!\n\n"
        f"**Registrar:** {KB['contacts']['registrar']}"
    )


def _fees(e):
    raw = e.get('_raw', '').lower()
    f  = KB['fees']
    u  = f['undergraduate']
    methods = '\n'.join(f"• {m}" for m in f['payment']['methods'])

    faculty_name = _detect_faculty(raw)
    specific_fee = ''
    if faculty_name in ('Engineering', 'Environmental Sciences'):
        specific_fee = f"\n**Your Faculty Estimate:** {u['tuition_ranges']['engineering_environmental']}"
    elif faculty_name in ('Medicine & Surgery', 'Pharmacy'):
        specific_fee = f"\n**Your Faculty Estimate:** {u['tuition_ranges']['medicine_pharmacy']}"
    elif faculty_name in ('Science', 'Education', 'Agriculture', 'Basic Medical Sciences'):
        specific_fee = f"\n**Your Faculty Estimate:** {u['tuition_ranges']['sciences_education']}"
    elif faculty_name in ('Management Sciences', 'Humanities & Social Sciences', 'Law'):
        specific_fee = f"\n**Your Faculty Estimate:** {u['tuition_ranges']['arts_management']}"

    return (
        f"**Fee Structure – {KB['university']['name']}**\n\n"
        f"**Undergraduate Tuition (per session):**\n"
        f"• Arts & Management Sciences: {u['tuition_ranges']['arts_management']}\n"
        f"• Sciences & Education: {u['tuition_ranges']['sciences_education']}\n"
        f"• Engineering & Environmental: {u['tuition_ranges']['engineering_environmental']}\n"
        f"• Medicine & Pharmacy: {u['tuition_ranges']['medicine_pharmacy']}\n"
        f"{specific_fee}\n\n"
        f"**Other Fees:**\n"
        f"• Acceptance Fee: {u['acceptance']}\n"
        f"• Hostel Fee: {u['hostel']}\n\n"
        f"**Payment Methods:**\n{methods}\n\n"
        f"• Portal: {f['payment']['portal']}\n"
        f"• Deadline: {f['payment']['deadline']}\n"
        f"• Tip: {f['payment']['tip']}\n\n"
        f"**{u['note']}**\n\n"
        f"**Bursary Contact:** {f['contact']}"
    )


def _exam(e):
    ex = KB['exams']
    rules  = '\n'.join(f'• {r}' for r in ex['rules'])
    grades = '\n'.join(f"• {score}: {grade}" for score, grade in ex['grading'].items())
    return (
        f"**Examinations – {KB['university']['name']}**\n\n"
        f"**Timetable:** {ex['schedule']}\n\n"
        f"**Exam Rules:**\n{rules}\n\n"
        f"**Grading System:**\n{grades}\n\n"
        f"**Resit / Carryover:** {ex['resit']}\n\n"
        f"**Results Release:** {ex['results_release']}\n\n"
        f"**Contact:** {ex['contact']}"
    )


def _results(e):
    raw = e.get('_raw', '').lower()

    if 'transcript' in raw:
        r = KB['results']
        return (
            "**Official Transcript – RSU**\n\n"
            f"{r['transcript']}\n\n"
            "**Steps:**\n"
            "1. Log in to the Student Portal\n"
            "2. Navigate to **Transcript Request**\n"
            "3. Pay the transcript processing fee\n"
            "4. Submit your application\n"
            "5. Collection takes 5–10 working days\n\n"
            f"**Exams Office:** {KB['exams']['contact']}\n"
            f"**Portal:** {KB['university']['ecampus']}"
        )

    if any(w in raw for w in ['cgpa', 'gpa', 'grade', 'classification', 'first class', 'second class', 'third class']):
        r = KB['results']
        classes = '\n'.join(f"• **{rng}** → {cls}" for rng, cls in r['classification'].items())
        return (
            f"**CGPA & Degree Classification – {KB['university']['name']}**\n\n"
            f"Graded on a **{r['cgpa_scale']}** scale:\n\n"
            f"{classes}\n\n"
            f"A CGPA of **{r['scholarship_cgpa']}** qualifies for most scholarships "
            "and competitive postgraduate programmes.\n\n"
            f"**Portal:** {r['portal']}"
        )

    return (
        "**Academic Results – RSU**\n\n"
        "Results are published on the **Student Portal** within 6 weeks after each exam period.\n\n"
        "**You can check:**\n"
        "• Semester results & grades\n"
        "• Cumulative GPA (CGPA)\n"
        "• Academic standing & probation status\n"
        "• Official transcripts\n\n"
        f"**Portal:** {KB['university']['ecampus']}\n"
        f"**Exams Office:** {KB['exams']['contact']}"
    )


def _hostel(_e):
    h = KB['hostel']
    types_ = '\n'.join(f'• {t}' for t in h['types'])
    rules  = '\n'.join(f'• {r}' for r in h['rules'])
    return (
        f"**Hostel & Accommodation – RSU**\n\n"
        f"{h['availability']}\n\n"
        f"**How to Apply:** {h['application']}\n\n"
        f"**Available Halls:**\n{types_}\n\n"
        f"**Hostel Rules:**\n{rules}\n\n"
        f"**Off-Campus Note:** {h['off_campus_note']}\n\n"
        f"**Contact:** {h['contact']}"
    )


def _library(_e):
    lib = KB['library']
    borrowing  = '\n'.join(f'• {who}: {limit}' for who, limit in lib['borrowing'].items())
    services   = '\n'.join(f'• {s}' for s in lib['services'])
    databases  = ', '.join(lib['databases'])
    return (
        f"**{lib['name']}**\n\n"
        f"**Opening Hours:**\n{lib['hours']}\n\n"
        f"**Borrowing Limits:**\n{borrowing}\n\n"
        f"**Overdue Fine:** {lib['fine']}\n\n"
        f"**E-Library:** {lib['eLibrary']}\n"
        f"**Available Databases:** {databases}\n\n"
        f"**Library Services:**\n{services}\n\n"
        f"**Contact:** {lib['contact']}"
    )


def _calendar(_e):
    cal = KB['calendar']
    return (
        f"**Academic Calendar – {KB['university']['name']}**\n\n"
        f"**Harmattan Semester:**\n"
        f"• Resumption: {cal['harmattan']['resumption']}\n"
        f"• Registration: {cal['harmattan']['registration']}\n"
        f"• Teaching: {cal['harmattan']['teaching']}\n"
        f"• Exams: {cal['harmattan']['exams']}\n\n"
        f"**Rain Semester:**\n"
        f"• Resumption: {cal['rain']['resumption']}\n"
        f"• Registration: {cal['rain']['registration']}\n"
        f"• Teaching: {cal['rain']['teaching']}\n"
        f"• Exams: {cal['rain']['exams']}\n\n"
        f"**Long Vacation:** {cal['long_vacation']}\n\n"
        f"**Note:** {cal['note']}\n\n"
        f"**Official Website:** {KB['university']['website']}\n"
        f"**News & Updates:** {KB['university']['news']}\n"
        f"**Events Calendar:** {KB['university']['events']}"
    )


def _contact(_e):
    c = KB['contacts']
    u = KB['university']
    return (
        f"**Key Contacts – {u['name']}**\n\n"
        f"**Registrar:** {c['registrar']}\n"
        f"**Bursary / Fees:** {c['bursary']}\n"
        f"**Student Affairs:** {c['studentAffairs']}\n"
        f"**Admissions:** {c['admissions']}\n"
        f"**Exams & Records:** {c['exams']}\n"
        f"**Library:** {c['library']}\n"
        f"**Accommodation:** {c['accommodation']}\n"
        f"**Health Centre:** {c['health']}\n"
        f"**ICT Support:** {c['ict']}\n"
        f"**Security:** {c['security']}\n\n"
        f"**Website:** {u['website']}\n"
        f"**Portal:** {u['ecampus']}\n"
        f"**Contact Page:** {u['contact_page']}\n"
        f"**General Email:** {c['general']}"
    )


def _scholarship(e):
    raw = e.get('_raw', '').lower()
    s = KB['scholarship']
    types_ = '\n'.join(f'• {t}' for t in s['types'])
    portals = '\n'.join(f"• {name}: {url}" for name, url in s['portals'].items())

    if 'nddc' in raw:
        return (
            "**NDDC Scholarship**\n\n"
            "The Niger Delta Development Commission (NDDC) offers scholarships to students "
            "from Niger Delta states (Rivers, Bayelsa, Delta, Akwa Ibom, Edo, Imo, Abia, Ondo, Cross River).\n\n"
            "**Requirement:** Proof of state of origin + good academic standing\n"
            f"**Portal:** {s['portals']['NDDC']}\n\n"
            f"**Contact:** {s['contact']}"
        )

    if 'ptdf' in raw:
        return (
            "**PTDF Scholarship**\n\n"
            "The Petroleum Technology Development Fund (PTDF) offers scholarships to students "
            "in petroleum, engineering, geoscience, and related courses.\n\n"
            "**Requirement:** Must be a full-time student in an eligible course\n"
            f"**Portal:** {s['portals']['PTDF']}\n\n"
            f"**Contact:** {s['contact']}"
        )

    if 'fgsb' in raw or 'federal' in raw:
        return (
            "**Federal Government Scholarship Board (FGSB)**\n\n"
            "The FGSB awards scholarships to academically outstanding Nigerian students.\n\n"
            "**Requirement:** Minimum CGPA of 3.5; strong academic record\n"
            f"**Portal:** {s['portals']['FGSB']}\n\n"
            f"**Contact:** {s['contact']}"
        )

    return (
        f"**Scholarships & Financial Aid – {KB['university']['name']}**\n\n"
        f"**Available Awards:**\n{types_}\n\n"
        f"**Requirements:** {s['requirements']}\n\n"
        f"**How to Apply:** {s['application']}\n\n"
        f"**Key Scholarship Portals:**\n{portals}\n\n"
        f"**Contact:** {s['contact']}"
    )


def _unknown(_e):
    return _p([
        "I'm not sure I understood that. Try asking about: **admission, fees, exams, results, hostel, library, courses, calendar, contacts,** or **scholarships**.",
        "Hmm, I didn't catch that. I can help with RSU university topics - fees, exams, hostel, admission, and more.",
        "Sorry, I couldn't understand your query. Please ask about a specific topic like **exam timetable**, **JAMB cutoff**, or **fee payment**.",
    ])


_HANDLERS = {
    'greeting':   _greeting,   'farewell':   _farewell,   'thanks':  _thanks,
    'help':       _help,       'admission':  _admission,  'courses': _courses,
    'fees':       _fees,       'exam':       _exam,       'results': _results,
    'hostel':     _hostel,     'library':    _library,    'calendar': _calendar,
    'contact':    _contact,    'scholarship': _scholarship,
}


def generate_response(intent: str, entities: dict = None) -> dict:
    handler = _HANDLERS.get(intent, _unknown)
    return {
        'text':        handler(entities or {}),
        'suggestions': SUGGESTIONS.get(intent, SUGGESTIONS['unknown']),
    }
