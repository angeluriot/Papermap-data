ID_TO_DOMAIN = {
	10: 'Multidisciplinary',
	11: 'Agricultural and Biological Sciences',
	12: 'Arts and Humanities',
	13: 'Biochemistry, Genetics and Molecular Biology',
	14: 'Business, Management and Accounting',
	15: 'Chemical Engineering',
	16: 'Chemistry',
	17: 'Computer Science',
	18: 'Decision Sciences',
	19: 'Earth and Planetary Sciences',
	20: 'Economics, Econometrics and Finance',
	21: 'Energy',
	22: 'Engineering',
	23: 'Environmental Science',
	24: 'Immunology and Microbiology',
	25: 'Materials Science',
	26: 'Mathematics',
	27: 'Medicine',
	28: 'Neuroscience',
	29: 'Nursing',
	30: 'Pharmacology, Toxicology and Pharmaceutics',
	31: 'Physics and Astronomy',
	32: 'Psychology',
	33: 'Social Sciences',
	34: 'Veterinary',
	35: 'Dentistry',
	36: 'Health Professions'
}

ID_TO_FIELD = {
	# Multidisciplinary
	1000: 'Multidisciplinary',

	# Agricultural and Biological Sciences
	1100: 'Agricultural and Biological Sciences',
	1101: 'Agricultural and Biological Sciences',
	1102: 'Agronomy and Crop Science',
	1103: 'Animal Science and Zoology',
	1104: 'Aquatic Science',
	1105: 'Ecology, Evolution, Behavior and Systematics',
	1106: 'Food Science',
	1107: 'Forestry',
	1108: 'Horticulture',
	1109: 'Insect Science',
	1110: 'Plant Science',
	1111: 'Soil Science',

	# Arts and Humanities
	1200: 'Arts and Humanities',
	1201: 'Arts and Humanities',
	1202: 'History',
	1203: 'Language and Linguistics',
	1204: 'Archeology (Arts and Humanities)',
	1205: 'Classics',
	1206: 'Conservation',
	1207: 'History and Philosophy of Science',
	1208: 'Literature and Literary Theory',
	1209: 'Museology',
	1210: 'Music',
	1211: 'Philosophy',
	1212: 'Religious Studies',
	1213: 'Visual Arts and Performing Arts',

	# Biochemistry, Genetics and Molecular Biology
	1300: 'Biochemistry, Genetics and Molecular Biology',
	1301: 'Biochemistry, Genetics and Molecular Biology',
	1302: 'Aging',
	1303: 'Biochemistry',
	1304: 'Biophysics',
	1305: 'Biotechnology',
	1306: 'Cancer Research',
	1307: 'Cell Biology',
	1308: 'Clinical Biochemistry',
	1309: 'Developmental Biology',
	1310: 'Endocrinology',
	1311: 'Genetics',
	1312: 'Molecular Biology',
	1313: 'Molecular Medicine',
	1314: 'Physiology',
	1315: 'Structural Biology',

	# Business, Management and Accounting
	1400: 'Business, Management and Accounting',
	1401: 'Business, Management and Accounting',
	1402: 'Accounting',
	1403: 'Business and International Management',
	1404: 'Management Information Systems',
	1405: 'Management of Technology and Innovation',
	1406: 'Marketing',
	1407: 'Organizational Behavior and Human Resource Management',
	1408: 'Strategy and Management',
	1409: 'Tourism, Leisure and Hospitality Management',
	1410: 'Industrial relations',

	# Chemical Engineering
	1500: 'Chemical Engineering',
	1501: 'Chemical Engineering',
	1502: 'Bioengineering',
	1503: 'Catalysis',
	1504: 'Chemical Health and Safety',
	1505: 'Colloid and Surface Chemistry',
	1506: 'Filtration and Separation',
	1507: 'Fluid Flow and Transfer Processes',
	1508: 'Process Chemistry and Technology',

	# Chemistry
	1600: 'Chemistry',
	1601: 'Chemistry',
	1602: 'Analytical Chemistry',
	1603: 'Electrochemistry',
	1604: 'Inorganic Chemistry',
	1605: 'Organic Chemistry',
	1606: 'Physical and Theoretical Chemistry',
	1607: 'Spectroscopy',

	# Computer Science
	1700: 'Computer Science',
	1701: 'Computer Science',
	1702: 'Artificial Intelligence',
	1703: 'Computational Theory and Mathematics',
	1704: 'Computer Graphics and Computer-Aided Design',
	1705: 'Computer Networks and Communications',
	1706: 'Computer Science Applications',
	1707: 'Computer Vision and Pattern Recognition',
	1708: 'Hardware and Architecture',
	1709: 'Human-Computer Interaction',
	1710: 'Information Systems',
	1711: 'Signal Processing',
	1712: 'Software',

	# Decision Sciences
	1800: 'Decision Sciences',
	1801: 'Decision Sciences',
	1802: 'Information Systems and Management',
	1803: 'Management Science and Operations Research',
	1804: 'Statistics, Probability and Uncertainty',

	# Earth and Planetary Sciences
	1900: 'Earth and Planetary Sciences',
	1901: 'Earth and Planetary Sciences',
	1902: 'Atmospheric Science',
	1903: 'Computers in Earth Sciences',
	1904: 'Earth-Surface Processes',
	1905: 'Economic Geology',
	1906: 'Geochemistry and Petrology',
	1907: 'Geology',
	1908: 'Geophysics',
	1909: 'Geotechnical Engineering and Engineering Geology',
	1910: 'Oceanography',
	1911: 'Paleontology',
	1912: 'Space and Planetary Science',
	1913: 'Stratigraphy',

	# Economics, Econometrics and Finance
	2000: 'Economics, Econometrics and Finance',
	2001: 'Economics, Econometrics and Finance',
	2002: 'Economics and Econometrics',
	2003: 'Finance',

	# Energy
	2100: 'Energy',
	2101: 'Energy',
	2102: 'Energy Engineering and Power Technology',
	2103: 'Fuel Technology',
	2104: 'Nuclear Energy and Engineering',
	2105: 'Renewable Energy, Sustainability and the Environment',

	# Engineering
	2200: 'Engineering',
	2201: 'Engineering',
	2202: 'Aerospace Engineering',
	2203: 'Automotive Engineering',
	2204: 'Biomedical Engineering',
	2205: 'Civil and Structural Engineering',
	2206: 'Computational Mechanics',
	2207: 'Control and Systems Engineering',
	2208: 'Electrical and Electronic Engineering',
	2209: 'Industrial and Manufacturing Engineering',
	2210: 'Mechanical Engineering',
	2211: 'Mechanics of Materials',
	2212: 'Ocean Engineering',
	2213: 'Safety, Risk, Reliability and Quality',
	2214: 'Media Technology',
	2215: 'Building and Construction',
	2216: 'Architecture',

	# Environmental Science
	2300: 'Environmental Science',
	2301: 'Environmental Science',
	2302: 'Ecological Modeling',
	2303: 'Ecology',
	2304: 'Environmental Chemistry',
	2305: 'Environmental Engineering',
	2306: 'Global and Planetary Change',
	2307: 'Health, Toxicology and Mutagenesis',
	2308: 'Management, Monitoring, Policy and Law',
	2309: 'Nature and Landscape Conservation',
	2310: 'Pollution',
	2311: 'Waste Management and Disposal',
	2312: 'Water Science and Technology',

	# Immunology and Microbiology
	2400: 'Immunology and Microbiology',
	2401: 'Immunology and Microbiology',
	2402: 'Applied Microbiology and Biotechnology',
	2403: 'Immunology',
	2404: 'Microbiology',
	2405: 'Parasitology',
	2406: 'Virology',

	# Materials Science
	2500: 'Materials Science',
	2501: 'Materials Science',
	2502: 'Biomaterials',
	2503: 'Ceramics and Composites',
	2504: 'Electronic, Optical and Magnetic Materials',
	2505: 'Materials Chemistry',
	2506: 'Metals and Alloys',
	2507: 'Polymers and Plastics',
	2508: 'Surfaces, Coatings and Films',
	2509: 'Nanoscience and Nanotechnology',

	# Mathematics
	2600: 'Mathematics',
	2601: 'Mathematics',
	2602: 'Algebra and Number Theory',
	2603: 'Analysis',
	2604: 'Applied Mathematics',
	2605: 'Computational Mathematics',
	2606: 'Control and Optimization',
	2607: 'Discrete Mathematics and Combinatorics',
	2608: 'Geometry and Topology',
	2609: 'Logic',
	2610: 'Mathematical Physics',
	2611: 'Modeling and Simulation',
	2612: 'Numerical Analysis',
	2613: 'Statistics and Probability',
	2614: 'Theoretical Computer Science',

	# Medicine
	2700: 'Medicine',
	2701: 'Medicine',
	2702: 'Anatomy',
	2703: 'Anesthesiology and Pain Medicine',
	2704: 'Biochemistry (Medical)',
	2705: 'Cardiology and Cardiovascular Medicine',
	2706: 'Critical Care and Intensive Care Medicine',
	2707: 'Complementary and Alternative Medicine',
	2708: 'Dermatology',
	2709: 'Drug Guides',
	2710: 'Embryology',
	2711: 'Emergency Medicine',
	2712: 'Endocrinology, Diabetes and Metabolism',
	2713: 'Epidemiology',
	2714: 'Family Practice',
	2715: 'Gastroenterology',
	2716: 'Genetics (Clinical)',
	2717: 'Geriatrics and Gerontology',
	2718: 'Health Informatics',
	2719: 'Health Policy',
	2720: 'Hematology',
	2721: 'Hepatology',
	2722: 'Histology',
	2723: 'Immunology and Allergy',
	2724: 'Internal Medicine',
	2725: 'Infectious Diseases',
	2726: 'Microbiology (Medical)',
	2727: 'Nephrology',
	2728: 'Neurology (Clinical)',
	2729: 'Obstetrics and Gynecology',
	2730: 'Oncology',
	2731: 'Ophthalmology',
	2732: 'Orthopedics and Sports Medicine',
	2733: 'Otorhinolaryngology',
	2734: 'Pathology and Forensic Medicine',
	2735: 'Pediatrics, Perinatology and Child Health',
	2736: 'Pharmacology (Medical)',
	2737: 'Physiology (Medical)',
	2738: 'Psychiatry and Mental health',
	2739: 'Public Health, Environmental and Occupational Health',
	2740: 'Pulmonary and Respiratory Medicine',
	2741: 'Radiology, Nuclear Medicine and imaging',
	2742: 'Rehabilitation',
	2743: 'Reproductive Medicine',
	2744: 'Reviews and References (Medical)',
	2745: 'Rheumatology',
	2746: 'Surgery',
	2747: 'Transplantation',
	2748: 'Urology',

	# Neuroscience
	2800: 'Neuroscience',
	2801: 'Neuroscience',
	2802: 'Behavioral Neuroscience',
	2803: 'Biological Psychiatry',
	2804: 'Cellular and Molecular Neuroscience',
	2805: 'Cognitive Neuroscience',
	2806: 'Developmental Neuroscience',
	2807: 'Endocrine and Autonomic Systems',
	2808: 'Neurology',
	2809: 'Sensory Systems',

	# Nursing
	2900: 'Nursing',
	2901: 'Nursing',
	2902: 'Advanced and Specialized Nursing',
	2903: 'Assessment and Diagnosis',
	2904: 'Care Planning',
	2905: 'Community and Home Care',
	2906: 'Critical Care Nursing',
	2907: 'Emergency Nursing',
	2908: 'Fundamentals and Skills',
	2909: 'Gerontology',
	2910: 'Issues, Ethics and Legal Aspects',
	2911: 'Leadership and Management',
	2912: 'LPN and LVN',
	2913: 'Maternity and Midwifery',
	2914: 'Medical and Surgical Nursing',
	2915: 'Nurse Assisting',
	2916: 'Nutrition and Dietetics',
	2917: 'Oncology (Nursing)',
	2918: 'Pathophysiology',
	2919: 'Pediatrics',
	2920: 'Pharmacology (Nursing)',
	2921: 'Pshychiatric Mental Health',
	2922: 'Research and Theory',
	2923: 'Review and Exam Preparation',

	# Pharmacology, Toxicology and Pharmaceutics
	3000: 'Pharmacology, Toxicology and Pharmaceutics',
	3001: 'Pharmacology, Toxicology and Pharmaceutics',
	3002: 'Drug Discovery',
	3003: 'Pharmaceutical Science',
	3004: 'Pharmacology',
	3005: 'Toxicology',

	# Physics and Astronomy
	3100: 'Physics and Astronomy',
	3101: 'Physics and Astronomy',
	3102: 'Acoustics and Ultrasonics',
	3103: 'Astronomy and Astrophysics',
	3104: 'Condensed Matter Physics',
	3105: 'Instrumentation',
	3106: 'Nuclear and High Energy Physics',
	3107: 'Atomic and Molecular Physics, and Optics',
	3108: 'Radiation',
	3109: 'Statistical and Nonlinear Physics',
	3110: 'Surfaces and Interfaces',

	# Psychology
	3200: 'Psychology',
	3201: 'Psychology',
	3202: 'Applied Psychology',
	3203: 'Clinical Psychology',
	3204: 'Developmental and Educational Psychology',
	3205: 'Experimental and Cognitive Psychology',
	3206: 'Neuropsychology and Physiological Psychology',
	3207: 'Social Psychology',

	# Social Sciences
	3300: 'Social Sciences',
	3301: 'Social Sciences',
	3302: 'Archeology',
	3303: 'Development',
	3304: 'Education',
	3305: 'Geography, Planning and Development',
	3306: 'Health (Social Science)',
	3307: 'Human Factors and Ergonomics',
	3308: 'Law',
	3309: 'Library and Information Sciences',
	3310: 'Linguistics and Language',
	3311: 'Safety Research',
	3312: 'Sociology and Political Science',
	3313: 'Transportation',
	3314: 'Anthropology',
	3315: 'Communication',
	3316: 'Cultural Studies',
	3317: 'Demography',
	3318: 'Gender Studies',
	3319: 'Life-span and Life-course Studies',
	3320: 'Political Science and International Relations',
	3321: 'Public Administration',
	3322: 'Urban Studies',
	3323: 'Social Work',
	3399: 'E-learning',

	# Veterinary
	3400: 'Veterinary',
	3401: 'Veterinary',
	3402: 'Equine',
	3403: 'Food Animals',
	3404: 'Small Animals',

	# Dentistry
	3500: 'Dentistry',
	3501: 'Dentistry',
	3502: 'Dental Assisting',
	3503: 'Dental Hygiene',
	3504: 'Oral Surgery',
	3505: 'Orthodontics',
	3506: 'Periodontics',

	# Health Professions
	3600: 'Health Professions',
	3601: 'Health Professions',
	3602: 'Chiropractics',
	3603: 'Complementary and Manual Therapy',
	3604: 'Emergency Medical Services',
	3605: 'Health Information Management',
	3606: 'Medical Assisting and Transcription',
	3607: 'Medical Laboratory Technology',
	3608: 'Medical Terminology',
	3609: 'Occupational Therapy',
	3610: 'Optometry',
	3611: 'Pharmacy',
	3612: 'Physical Therapy, Sports Therapy and Rehabilitation',
	3613: 'Podiatry',
	3614: 'Radiological and Ultrasound Technology',
	3615: 'Respiratory Care',
	3616: 'Speech and Hearing',
	3699: 'Sports Science'
}

DOMAIN_TO_ID = {name.lower(): code for code, name in ID_TO_DOMAIN.items()}
FIELD_TO_ID = {name.lower(): code for code, name in ID_TO_FIELD.items()}

FIELDS = {
	'Multidisciplinary': [],

	'Agricultural and Biological Sciences': [
		'Agronomy and Crop Science',
		'Animal Science and Zoology',
		'Aquatic Science',
		'Ecology, Evolution, Behavior and Systematics',
		'Food Science',
		'Forestry',
		'Horticulture',
		'Insect Science',
		'Plant Science',
		'Soil Science'
	],

	'Arts and Humanities': [
		'History',
		'Language and Linguistics',
		'Archeology (Arts and Humanities)',
		'Classics',
		'Conservation',
		'History and Philosophy of Science',
		'Literature and Literary Theory',
		'Museology',
		'Music',
		'Philosophy',
		'Religious Studies',
		'Visual Arts and Performing Arts'
	],

	'Biochemistry, Genetics and Molecular Biology': [
		'Aging',
		'Biochemistry',
		'Biophysics',
		'Biotechnology',
		'Cancer Research',
		'Cell Biology',
		'Clinical Biochemistry',
		'Developmental Biology',
		'Endocrinology',
		'Genetics',
		'Molecular Biology',
		'Molecular Medicine',
		'Physiology',
		'Structural Biology'
	],

	'Business, Management and Accounting': [
		'Accounting',
		'Business and International Management',
		'Management Information Systems',
		'Management of Technology and Innovation',
		'Marketing',
		'Organizational Behavior and Human Resource Management',
		'Strategy and Management',
		'Tourism, Leisure and Hospitality Management',
		'Industrial relations'
	],

	'Chemical Engineering': [
		'Bioengineering',
		'Catalysis',
		'Chemical Health and Safety',
		'Colloid and Surface Chemistry',
		'Filtration and Separation',
		'Fluid Flow and Transfer Processes',
		'Process Chemistry and Technology'
	],

	'Chemistry': [
		'Analytical Chemistry',
		'Electrochemistry',
		'Inorganic Chemistry',
		'Organic Chemistry',
		'Physical and Theoretical Chemistry',
		'Spectroscopy'
	],

	'Computer Science': [
		'Artificial Intelligence',
		'Computational Theory and Mathematics',
		'Computer Graphics and Computer-Aided Design',
		'Computer Networks and Communications',
		'Computer Science Applications',
		'Computer Vision and Pattern Recognition',
		'Hardware and Architecture',
		'Human-Computer Interaction',
		'Information Systems',
		'Signal Processing',
		'Software'
	],

	'Decision Sciences': [
		'Information Systems and Management',
		'Management Science and Operations Research',
		'Statistics, Probability and Uncertainty'
	],

	'Earth and Planetary Sciences': [
		'Atmospheric Science',
		'Computers in Earth Sciences',
		'Earth-Surface Processes',
		'Economic Geology',
		'Geochemistry and Petrology',
		'Geology',
		'Geophysics',
		'Geotechnical Engineering and Engineering Geology',
		'Oceanography',
		'Paleontology',
		'Space and Planetary Science',
		'Stratigraphy'
	],

	'Economics, Econometrics and Finance': [
		'Economics and Econometrics',
		'Finance'
	],

	'Energy': [
		'Energy Engineering and Power Technology',
		'Fuel Technology',
		'Nuclear Energy and Engineering',
		'Renewable Energy, Sustainability and the Environment'
	],

	'Engineering': [
		'Aerospace Engineering',
		'Automotive Engineering',
		'Biomedical Engineering',
		'Civil and Structural Engineering',
		'Computational Mechanics',
		'Control and Systems Engineering',
		'Electrical and Electronic Engineering',
		'Industrial and Manufacturing Engineering',
		'Mechanical Engineering',
		'Mechanics of Materials',
		'Ocean Engineering',
		'Safety, Risk, Reliability and Quality',
		'Media Technology',
		'Building and Construction',
		'Architecture'
	],

	'Environmental Science': [
		'Ecological Modeling',
		'Ecology',
		'Environmental Chemistry',
		'Environmental Engineering',
		'Global and Planetary Change',
		'Health, Toxicology and Mutagenesis',
		'Management, Monitoring, Policy and Law',
		'Nature and Landscape Conservation',
		'Pollution',
		'Waste Management and Disposal',
		'Water Science and Technology'
	],

	'Immunology and Microbiology': [
		'Applied Microbiology and Biotechnology',
		'Immunology',
		'Microbiology',
		'Parasitology',
		'Virology'
	],

	'Materials Science': [
		'Biomaterials',
		'Ceramics and Composites',
		'Electronic, Optical and Magnetic Materials',
		'Materials Chemistry',
		'Metals and Alloys',
		'Polymers and Plastics',
		'Surfaces, Coatings and Films',
		'Nanoscience and Nanotechnology'
	],

	'Mathematics': [
		'Algebra and Number Theory',
		'Analysis',
		'Applied Mathematics',
		'Computational Mathematics',
		'Control and Optimization',
		'Discrete Mathematics and Combinatorics',
		'Geometry and Topology',
		'Logic',
		'Mathematical Physics',
		'Modeling and Simulation',
		'Numerical Analysis',
		'Statistics and Probability',
		'Theoretical Computer Science'
	],

	'Medicine': [
		'Anatomy',
		'Anesthesiology and Pain Medicine',
		'Biochemistry (Medical)',
		'Cardiology and Cardiovascular Medicine',
		'Critical Care and Intensive Care Medicine',
		'Complementary and Alternative Medicine',
		'Dermatology',
		'Drug Guides',
		'Embryology',
		'Emergency Medicine',
		'Endocrinology, Diabetes and Metabolism',
		'Epidemiology',
		'Family Practice',
		'Gastroenterology',
		'Genetics (Clinical)',
		'Geriatrics and Gerontology',
		'Health Informatics',
		'Health Policy',
		'Hematology',
		'Hepatology',
		'Histology',
		'Immunology and Allergy',
		'Internal Medicine',
		'Infectious Diseases',
		'Microbiology (Medical)',
		'Nephrology',
		'Neurology (Clinical)',
		'Obstetrics and Gynecology',
		'Oncology',
		'Ophthalmology',
		'Orthopedics and Sports Medicine',
		'Otorhinolaryngology',
		'Pathology and Forensic Medicine',
		'Pediatrics, Perinatology and Child Health',
		'Pharmacology (Medical)',
		'Physiology (Medical)',
		'Psychiatry and Mental health',
		'Public Health, Environmental and Occupational Health',
		'Pulmonary and Respiratory Medicine',
		'Radiology, Nuclear Medicine and imaging',
		'Rehabilitation',
		'Reproductive Medicine',
		'Reviews and References (Medical)',
		'Rheumatology',
		'Surgery',
		'Transplantation',
		'Urology'
	],

	'Neuroscience': [
		'Behavioral Neuroscience',
		'Biological Psychiatry',
		'Cellular and Molecular Neuroscience',
		'Cognitive Neuroscience',
		'Developmental Neuroscience',
		'Endocrine and Autonomic Systems',
		'Neurology',
		'Sensory Systems'
	],

	'Nursing': [
		'Advanced and Specialized Nursing',
		'Assessment and Diagnosis',
		'Care Planning',
		'Community and Home Care',
		'Critical Care Nursing',
		'Emergency Nursing',
		'Fundamentals and Skills',
		'Gerontology',
		'Issues, Ethics and Legal Aspects',
		'Leadership and Management',
		'LPN and LVN',
		'Maternity and Midwifery',
		'Medical and Surgical Nursing',
		'Nurse Assisting',
		'Nutrition and Dietetics',
		'Oncology (Nursing)',
		'Pathophysiology',
		'Pediatrics',
		'Pharmacology (Nursing)',
		'Pshychiatric Mental Health',
		'Research and Theory',
		'Review and Exam Preparation'
	],

	'Pharmacology, Toxicology and Pharmaceutics': [
		'Drug Discovery',
		'Pharmaceutical Science',
		'Pharmacology',
		'Toxicology'
	],

	'Physics and Astronomy': [
		'Acoustics and Ultrasonics',
		'Astronomy and Astrophysics',
		'Condensed Matter Physics',
		'Instrumentation',
		'Nuclear and High Energy Physics',
		'Atomic and Molecular Physics, and Optics',
		'Radiation',
		'Statistical and Nonlinear Physics',
		'Surfaces and Interfaces'
	],

	'Psychology': [
		'Applied Psychology',
		'Clinical Psychology',
		'Developmental and Educational Psychology',
		'Experimental and Cognitive Psychology',
		'Neuropsychology and Physiological Psychology',
		'Social Psychology'
	],

	'Social Sciences': [
		'Archeology',
		'Development',
		'Education',
		'Geography, Planning and Development',
		'Health (Social Science)',
		'Human Factors and Ergonomics',
		'Law',
		'Library and Information Sciences',
		'Linguistics and Language',
		'Safety Research',
		'Sociology and Political Science',
		'Transportation',
		'Anthropology',
		'Communication',
		'Cultural Studies',
		'Demography',
		'Gender Studies',
		'Life-span and Life-course Studies',
		'Political Science and International Relations',
		'Public Administration',
		'Urban Studies',
		'Social Work',
		'E-learning'
	],

	'Veterinary': [
		'Equine',
		'Food Animals',
		'Small Animals'
	],

	'Dentistry': [
		'Dental Assisting',
		'Dental Hygiene',
		'Oral Surgery',
		'Orthodontics',
		'Periodontics'
	],

	'Health Professions': [
		'Chiropractics',
		'Complementary and Manual Therapy',
		'Emergency Medical Services',
		'Health Information Management',
		'Medical Assisting and Transcription',
		'Medical Laboratory Technology',
		'Medical Terminology',
		'Occupational Therapy',
		'Optometry',
		'Pharmacy',
		'Physical Therapy, Sports Therapy and Rehabilitation',
		'Podiatry',
		'Radiological and Ultrasound Technology',
		'Respiratory Care',
		'Speech and Hearing',
		'Sports Science'
	]
}
