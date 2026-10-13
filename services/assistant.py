FAQS = [
    {
        "keywords": ["income certificate", "income proof"],
        "answer": "For an income certificate, check your state government's official service portal or the relevant revenue office. Required documents and processing times vary by state.",
        "url": "https://services.india.gov.in/"
    },
    {
        "keywords": ["scholarship", "student aid"],
        "answer": "You can explore eligible scholarship opportunities on the National Scholarship Portal. Read the current scheme guidelines before applying.",
        "url": "https://scholarships.gov.in/"
    },
    {
        "keywords": ["farmer", "pm kisan", "agriculture"],
        "answer": "For farmer-related support and PM-KISAN information, use the official PM-KISAN portal and verify current eligibility requirements.",
        "url": "https://pmkisan.gov.in/"
    },
    {
        "keywords": ["complaint", "grievance", "complain"],
        "answer": "You can submit a demo grievance through the SmartGov AI Grievance Management module. This prototype creates a local ticket and does not forward complaints to a government department.",
        "url": "https://pgportal.gov.in/"
    },
    {
        "keywords": ["application status", "track application", "tracking"],
        "answer": "Use the Application Tracker with your reference number. This prototype only recognizes sample IDs such as SG-1001, SG-1002, and SG-1003.",
        "url": "https://services.india.gov.in/"
    },
    {
        "keywords": ["umang", "government services", "digital service"],
        "answer": "UMANG provides access to a range of government services. Service availability varies by department.",
        "url": "https://web.umang.gov.in/"
    }
]

TRANSLATIONS = {
    "Hindi": "यह SmartGov AI का डेमो उत्तर है। कृपया संबंधित सरकारी पोर्टल पर नवीनतम जानकारी और पात्रता की पुष्टि करें।",
    "Marathi": "हे SmartGov AI चे प्रात्यक्षिक उत्तर आहे. कृपया संबंधित अधिकृत सरकारी पोर्टलवर नवीनतम माहिती आणि पात्रता तपासा."
}

def answer_question(question, language="English"):
    q = question.lower()
    for item in FAQS:
        if any(keyword in q for keyword in item["keywords"]):
            answer = item["answer"]
            if language in ("Hindi", "Marathi"):
                answer = TRANSLATIONS[language] + "\n\n" + answer
            return {
                "answer": answer,
                "source_url": item["url"],
                "language": language,
                "disclaimer": "Prototype FAQ matching; not an official government response."
            }
    fallback = "I couldn't find a matching topic in the demo FAQ. Try asking about scholarships, farmer support, application tracking, income certificates, grievances, or UMANG."
    if language in ("Hindi", "Marathi"):
        fallback = TRANSLATIONS[language] + "\n\n" + fallback
    return {
        "answer": fallback,
        "source_url": "https://www.india.gov.in/",
        "language": language,
        "disclaimer": "Verify important information through official sources."
    }
