import json
import os

KB = {
    'university': {
        'name': 'Rivers State University',
        'abbreviation': 'RSU',
        'formerly': 'Rivers State University of Science and Technology (RSUST)',
        'founded': '1980',
        'website': 'https://www.rsu.edu.ng',
        'ecampus': 'https://ecampus.rsu.edu.ng',
        'about': 'https://www.rsu.edu.ng/about-us/',
        'contact_page': 'https://www.rsu.edu.ng/contact/',
        'news': 'https://www.rsu.edu.ng/news-update/',
        'events': 'https://www.rsu.edu.ng/event-calendar/',
        'email': 'info@rsu.edu.ng',
        'phone': '+234 810 444 4411',
        'address': 'Nkpolu – Oroworukwo, P.M.B. 5080, Port Harcourt, Rivers State, Nigeria',
        'motto': 'Knowledge for Service',
        'type': 'State University',
        'state': 'Rivers State, Nigeria',
        'city': 'Port Harcourt',
    },

    'admission': {
        'requirements': [
            "Five (5) O'Level credits including English Language and Mathematics (obtained in not more than two sittings)",
            'Valid JAMB UTME score - minimum 180 for most courses; 200+ for Medicine, Law, and Pharmacy',
            'Pass the RSU Post-UTME screening (Computer-Based Test)',
            'Minimum age of 16 years at point of entry',
            "Direct Entry: Minimum of two (2) A'Level passes or OND/NCE (upper credit) in relevant subjects",
        ],
        'process': [
            'Purchase the RSU Post-UTME form on ecampus.rsu.edu.ng during the application window',
            "Upload required documents: O'Level result, JAMB result slip, birth certificate, passport photograph",
            'Sit for and pass the RSU Post-UTME screening (CBT format)',
            'Check your admission status on JAMB CAPS (caps.jamb.gov.ng) and the RSU e-campus portal',
            'Accept your admission offer on JAMB CAPS within the stated deadline',
            'Pay the acceptance fee on ecampus.rsu.edu.ng',
            'Complete your departmental and faculty registration',
            'Attend the mandatory matriculation ceremony',
        ],
        'jamb_cutoff': {
            'general_minimum': 180,
            'medicine_surgery': 200,
            'pharmacy': 200,
            'law': 200,
            'engineering': 180,
            'sciences': 180,
            'management_sciences': 160,
            'arts_humanities': 160,
            'education': 160,
            'agriculture': 160,
            'environmental_sciences': 160,
        },
        'post_utme': (
            'RSU Post-UTME is a Computer-Based Test (CBT). '
            'It covers English Language, Mathematics, and subjects relevant to your chosen course. '
            'A score of 50% and above is generally required to be considered.'
        ),
        'deadline': 'Application deadlines are published on the RSU e-campus portal at the start of each admissions cycle.',
        'contact': 'admissions@rsu.edu.ng | +234 810 444 4411',
        'portal': 'https://ecampus.rsu.edu.ng',
    },

    'faculties': {
        'Engineering': {
            'full_name': 'Faculty of Engineering',
            'departments': [
                'Civil Engineering',
                'Mechanical Engineering',
                'Electrical / Electronic Engineering',
                'Chemical Engineering',
                'Agricultural Engineering',
                'Petroleum & Gas Engineering',
                'Marine Engineering',
                'Computer Engineering',
            ],
            'jamb_subjects': 'Mathematics, Physics, Chemistry + English Language',
            'degree': 'B.Eng',
            'duration': '5 years',
        },
        'Science': {
            'full_name': 'Faculty of Natural & Applied Sciences',
            'departments': [
                'Mathematics',
                'Physics',
                'Chemistry',
                'Biology',
                'Computer Science',
                'Geology',
                'Microbiology',
                'Biochemistry',
                'Statistics',
                'Industrial Chemistry',
            ],
            'jamb_subjects': 'Mathematics/Biology, Physics, Chemistry + English Language (varies by department)',
            'degree': 'B.Sc',
            'duration': '4 years',
        },
        'Management Sciences': {
            'full_name': 'Faculty of Management Sciences',
            'departments': [
                'Accounting',
                'Business Administration',
                'Banking & Finance',
                'Marketing',
                'Public Administration',
                'Insurance',
            ],
            'jamb_subjects': 'Economics, Mathematics, English Language + one Social Science subject',
            'degree': 'B.Sc',
            'duration': '4 years',
        },
        'Humanities & Social Sciences': {
            'full_name': 'Faculty of Humanities & Social Sciences',
            'departments': [
                'English Language & Literary Studies',
                'History & Diplomatic Studies',
                'Philosophy',
                'Religious & Cultural Studies',
                'Theatre & Film Studies',
                'Mass Communication',
                'Political Science & Administrative Studies',
                'Sociology',
                'Psychology',
                'French & International Studies',
                'Economics',
            ],
            'jamb_subjects': 'English Language + three (3) Arts or Social Science subjects',
            'degree': 'B.A / B.Sc',
            'duration': '4 years',
        },
        'Law': {
            'full_name': 'Faculty of Law',
            'departments': [
                'Jurisprudence & International Law',
                'Private & Property Law',
                'Public Law',
            ],
            'jamb_subjects': 'English Language, Literature-in-English + two other Arts subjects',
            'degree': 'LLB',
            'duration': '5 years',
            'note': 'After graduation, students must attend the Nigerian Law School to obtain the BL certificate before being called to Bar.',
        },
        'Agriculture': {
            'full_name': 'Faculty of Agriculture',
            'departments': [
                'Agricultural Economics & Extension',
                'Animal Science & Fisheries',
                'Crop & Soil Science',
                'Forestry & Environmental Management',
            ],
            'jamb_subjects': 'Biology/Agriculture, Chemistry, Physics/Mathematics + English Language',
            'degree': 'B.Agric / B.Sc',
            'duration': '4–5 years',
        },
        'Environmental Sciences': {
            'full_name': 'Faculty of Environmental Sciences',
            'departments': [
                'Urban & Regional Planning',
                'Architecture',
                'Building Technology',
                'Quantity Surveying',
                'Estate Management',
            ],
            'jamb_subjects': 'Mathematics, Physics, Chemistry/Geography + English Language',
            'degree': 'B.Sc / B.Tech',
            'duration': '5 years',
        },
        'Education': {
            'full_name': 'Faculty of Education',
            'departments': [
                'Educational Management & Planning',
                'Guidance & Counselling',
                'Curriculum Studies & Educational Technology',
                'Science & Mathematics Education',
                'Arts & Social Science Education',
                'Technical & Vocational Education',
            ],
            'jamb_subjects': 'English Language + three subjects relevant to your teaching specialisation',
            'degree': 'B.Ed / B.Sc (Ed)',
            'duration': '4 years',
        },
        'Medicine & Surgery': {
            'full_name': 'College of Health Sciences – Medicine & Surgery',
            'departments': ['Medicine & Surgery (MBBS)'],
            'jamb_subjects': 'Biology, Chemistry, Physics + English Language',
            'degree': 'MBBS',
            'duration': '6 years',
            'note': 'Minimum JAMB score of 200 required. The programme includes 3 years pre-clinical and 3 years clinical rotation in RSU Teaching Hospital.',
        },
        'Pharmacy': {
            'full_name': 'Faculty of Pharmacy',
            'departments': ['Pharmacy (B.Pharm)'],
            'jamb_subjects': 'Chemistry, Biology, Physics/Mathematics + English Language',
            'degree': 'B.Pharm',
            'duration': '5 years',
        },
        'Basic Medical Sciences': {
            'full_name': 'College of Basic Medical Sciences',
            'departments': ['Anatomy', 'Physiology', 'Pharmacology'],
            'jamb_subjects': 'Biology, Chemistry, Physics + English Language',
            'degree': 'B.Sc',
            'duration': '4 years',
        },
    },

    'fees': {
        'undergraduate': {
            'note': 'RSU fees are updated every session. The figures below are estimates - always confirm on ecampus.rsu.edu.ng.',
            'tuition_ranges': {
                'arts_management': 'Approx. ₦100,000 – ₦150,000 per session',
                'sciences_education': 'Approx. ₦120,000 – ₦180,000 per session',
                'engineering_environmental': 'Approx. ₦150,000 – ₦250,000 per session',
                'medicine_pharmacy': 'Approx. ₦300,000 – ₦500,000 per session',
            },
            'acceptance': 'Approx. ₦50,000 (confirm on portal)',
            'hostel': 'Approx. ₦30,000 – ₦60,000 per session (check accommodation office)',
            'medical_levy': 'Included in student levies - see portal',
        },
        'payment': {
            'portal': 'ecampus.rsu.edu.ng',
            'methods': [
                'Remita payment platform (recommended) - https://remita.net',
                'Online card payment via the RSU e-campus portal',
                'Bank deposit with RSU teller at designated banks',
            ],
            'deadline': 'Within the first 4 weeks of each semester',
            'tip': 'Always save your Remita Retrieval Reference (RRR) number as proof of payment.',
        },
        'contact': 'bursary@rsu.edu.ng | +234 810 444 4411',
    },

    'exams': {
        'schedule': 'Exam timetables are released on the RSU e-campus portal approximately 3 weeks before exams begin.',
        'rules': [
            'Arrive at least 30 minutes before the exam start time',
            'Present your valid student ID card and exam slip at the hall entrance',
            'No electronic devices (phones, smart watches, unauthorised calculators) in the exam hall',
            'Late entry is not permitted 30 minutes after the exam starts',
            'Examination malpractice results in cancellation of that paper and may lead to expulsion',
            'Dress code must be observed - no hats, hoods, or dark glasses in the hall',
            'Candidates must sign the attendance register before collecting their scripts',
        ],
        'grading': {
            '70 – 100': 'A – Excellent (5 grade points)',
            '60 – 69':  'B – Good (4 grade points)',
            '50 – 59':  'C – Average (3 grade points)',
            '45 – 49':  'D – Below Average (2 grade points)',
            '40 – 44':  'E – Pass (1 grade point)',
            '0 – 39':   'F – Fail (0 grade points)',
        },
        'resit': 'Carryover/resit exams are held at the start of the following semester. Register via the RSU e-campus portal.',
        'results_release': 'Results are published on ecampus.rsu.edu.ng within 6 weeks after each exam period.',
        'contact': 'exams@rsu.edu.ng | +234 810 444 4411',
    },

    'results': {
        'cgpa_scale': '5.0 point scale',
        'classification': {
            '4.50 – 5.00': 'First Class Honours',
            '3.50 – 4.49': 'Second Class Upper (2:1)',
            '2.40 – 3.49': 'Second Class Lower (2:2)',
            '1.50 – 2.39': 'Third Class',
            '1.00 – 1.49': 'Pass',
            'Below 1.00':  'Probation / Possible Withdrawal',
        },
        'scholarship_cgpa': '3.50 and above (on 5.0 scale)',
        'portal': 'https://ecampus.rsu.edu.ng',
        'transcript': 'Apply via the Exams & Records Office or the Student Portal. A transcript fee applies. Allow 5-10 working days.',
    },

    'hostel': {
        'availability': 'On-campus accommodation is limited and allocated on a first-come, first-served basis each session.',
        'application': 'Apply via ecampus.rsu.edu.ng during the accommodation application window.',
        'types': [
            'Male Halls of Residence',
            'Female Halls of Residence',
            'Postgraduate Hostels',
        ],
        'rules': [
            'Quiet hours: 10 PM – 6 AM (strictly enforced)',
            'No visitors of the opposite sex after 8 PM',
            'Smoking and alcohol are strictly prohibited on campus',
            'Keep your room and surroundings clean at all times',
            'Cooking with open flames (kerosene stoves) is prohibited in rooms',
            'Tampering with electrical fittings is a punishable offence',
            'Loss of hostel accommodation can result from rule violations',
        ],
        'off_campus_note': 'Many students live off-campus in nearby areas: Nkpolu, Rumuola, Rumuomasi, and D/Line in Port Harcourt.',
        'contact': 'accommodation@rsu.edu.ng | +234 810 444 4411',
    },

    'library': {
        'name': 'RSU Main Library',
        'hours': 'Mon – Fri: 8:00 AM – 10:00 PM  |  Saturday: 9:00 AM – 6:00 PM  |  Sunday: Closed',
        'borrowing': {
            'Undergraduate': '3 books for 2 weeks',
            'Postgraduate':  '5 books for 4 weeks',
            'Academic Staff': '7 books for 8 weeks',
        },
        'fine': '₦20 per book per day for overdue items (check library notice board for current rates)',
        'eLibrary': 'Available via ecampus.rsu.edu.ng - access journals, e-books, and research databases',
        'databases': ['JSTOR', 'EBSCOhost', 'African Journals Online (AJOL)', 'ResearchGate', 'Google Scholar'],
        'services': [
            'Book borrowing and reference services',
            'Internet access and computer workstations',
            'Photocopying and printing services',
            'E-library and online academic database access',
            'Research support and referencing assistance',
            'Quiet study rooms and reading areas',
        ],
        'contact': 'library@rsu.edu.ng | +234 810 444 4411',
    },

    'calendar': {
        'harmattan': {
            'resumption': 'October',
            'registration': 'October – November',
            'teaching': 'November – December',
            'exams': 'January – February',
            'end': 'February',
        },
        'rain': {
            'resumption': 'March',
            'registration': 'March – April',
            'teaching': 'April – May',
            'exams': 'June – July',
            'end': 'July',
        },
        'long_vacation': 'August – September (between Rain and Harmattan semesters)',
        'note': 'Exact dates are published each session on www.rsu.edu.ng and ecampus.rsu.edu.ng. Dates may shift due to ASUU or public events.',
    },

    'departments': [
        'Engineering', 'Medicine & Surgery', 'Law', 'Sciences',
        'Arts & Social Sciences', 'Agriculture', 'Education',
        'Management Sciences', 'Pharmacy', 'Environmental Sciences',
        'Basic Medical Sciences', 'Clinical Sciences',
    ],

    'contacts': {
        'registrar':       'registrar@rsu.edu.ng | +234 810 444 4411',
        'bursary':         'bursary@rsu.edu.ng | +234 810 444 4411',
        'studentAffairs':  'studentaffairs@rsu.edu.ng | +234 810 444 4411',
        'health':          'health@rsu.edu.ng | +234 810 444 4411',
        'security':        '+234 810 444 4411',
        'ict':             'ict@rsu.edu.ng | +234 810 444 4411',
        'admissions':      'admissions@rsu.edu.ng | +234 810 444 4411',
        'exams':           'exams@rsu.edu.ng | +234 810 444 4411',
        'library':         'library@rsu.edu.ng | +234 810 444 4411',
        'accommodation':   'accommodation@rsu.edu.ng | +234 810 444 4411',
        'scholarships':    'scholarships@rsu.edu.ng | +234 810 444 4411',
        'general':         'info@rsu.edu.ng | +234 810 444 4411',
        'website':         'https://www.rsu.edu.ng',
        'portal':          'https://ecampus.rsu.edu.ng',
    },

    'scholarship': {
        'types': [
            'Federal Government Scholarship Board (FGSB) Award - for academically outstanding students nationwide',
            'Rivers State Government Bursary Award - ₦5,000–₦20,000 per session for Rivers State indigenes',
            'RSU Merit Scholarship - for top-performing students per faculty (minimum 4.0 CGPA)',
            'Niger Delta Development Commission (NDDC) Scholarship - for Niger Delta students in Science & Engineering',
            'Shell Nigeria Scholarship - for students in Science, Engineering, and related disciplines',
            'Agip/ENI Nigeria Scholarship - for students in STEM and Management courses',
            'Petroleum Technology Development Fund (PTDF) - for petroleum-related and engineering courses',
            'Faculty-level grants and external donor scholarships (check Student Affairs office)',
        ],
        'requirements': (
            'Minimum CGPA of 3.5 on a 5.0 scale for most awards. '
            'NDDC and Rivers State bursary require proof of indigeneship (state of origin certificate). '
            'PTDF is for full-time students in petroleum and engineering courses.'
        ),
        'application': (
            'Apply through the RSU Student Affairs office or via ecampus.rsu.edu.ng. '
            'FGSB and PTDF require separate applications on their official portals.'
        ),
        'portals': {
            'FGSB': 'https://scholarship.gov.ng',
            'NDDC': 'https://nddc.gov.ng',
            'PTDF': 'https://ptdf.gov.ng',
        },
        'contact': 'scholarships@rsu.edu.ng | +234 810 444 4411',
    },

    'scraped': {},
}


# ── Load scraped RSU data if available ─────────────────────────────────────
_scraped_path = os.path.join(os.path.dirname(__file__), 'scraped_rsu.json')

if os.path.exists(_scraped_path):
    with open(_scraped_path, 'r', encoding='utf-8') as _f:
        KB['scraped'] = json.load(_f)
    print(f"[KB] Loaded scraped data: {len(KB['scraped'])} pages")
else:
    print('[KB] Running on curated RSU knowledge base.')
