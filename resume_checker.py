import requests
import os
import fitz
import PyPDF2
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


resume_keywords = {
    "App Developer": [
        "Android", "Flutter", "Dart", "Kotlin", "iOS", "Swift", "Java", "React Native"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Angular", "Vue", "Node.js", "Bootstrap", "SASS", "Web Development"
    ],
    "Data Scientist": [
        "Python", "R", "Pandas", "NumPy", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Data Analysis", "Data Visualization"
    ],
    "Cyber Security Analyst": [
        "Cyber Security", "Network Security", "Firewalls", "Intrusion Detection", "Penetration Testing", "Blockchain", "Encryption", "Threat Analysis"
    ],
    "Product Manager": [
        "Product Management", "Roadmap", "Scrum", "Agile", "User Stories", "Market Research", "Stakeholder Management", "MVP", "A/B Testing"
    ],
    "Software Engineer": [
        "Software Development", "Java", "C++", "Python", "Algorithms", "Data Structures", "Software Design", "Version Control", "Agile"
    ],
    "DevOps Engineer": [
        "DevOps", "CI/CD", "Jenkins", "Docker", "Kubernetes", "AWS", "Azure", "Ansible", "Infrastructure as Code", "Terraform"
    ],
    "Machine Learning Engineer": [
        "Machine Learning", "Deep Learning", "Python", "Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "Model Deployment", "Feature Engineering"
    ],
    "UI/UX Designer": [
        "User Interface", "User Experience", "Wireframes", "Prototyping", "Adobe XD", "Figma", "Sketch", "Usability Testing", "Interaction Design"
    ],
    "Cloud Engineer": [
        "Cloud Computing", "AWS", "Azure", "Google Cloud", "Kubernetes", "Cloud Security", "Serverless", "Cloud Architecture", "DevOps"
    ],
    "Blockchain Developer": [
        "Blockchain", "Smart Contracts", "Ethereum", "Solidity", "Hyperledger", "Cryptocurrency", "Decentralized Applications", "Consensus Algorithms"
    ],
    
    "Default":[
        "Blockchain", "Smart Contracts", "Ethereum", "Solidity", "Hyperledger", "Cryptocurrency", "Decentralized Applications", "Consensus Algorithms"
    ]
    
}


def download_pdf(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("PDF downloaded successfully.")
        return 0
    else:
        print("Failed to download PDF.")
        return -1

def delete_pdf(save_path):
    if os.path.exists(save_path):
        os.remove(save_path)
        print("PDF deleted successfully.")
    else:
        print("File not found. No PDF deleted.")

def extract_text_from_pdf(save_path):
    with open(save_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"
    return text

def evaluate_cv(url, save_path, resume_type):

    status = download_pdf(url, save_path)
    # if status == -1:
    #     print("Failed to process the CV.")
    #     return status, ""
    
    text = extract_text_from_pdf(save_path)
    delete_pdf(save_path)

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Validate resume type
    if resume_type not in resume_keywords:
        resume_type="Default"
    
    keywords_lower = {keyword.lower() for keyword in resume_keywords[resume_type]}

    matching_keywords = {token for token in filtered_tokens if token in keywords_lower}

    non_matching_keywords = keywords_lower - matching_keywords

    if len(keywords_lower) == 0:
        return float('inf')  
    else:
        score = round((len(matching_keywords) / len(keywords_lower)) * 5, 1)
        return score, non_matching_keywords

def determine_resume_type(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    scores = {}

    for resume_type, keywords in resume_keywords.items():
        keywords_lower = {keyword.lower() for keyword in keywords}
        matching_keywords = {token for token in filtered_tokens if token in keywords_lower}
        score = len(matching_keywords)
        scores[resume_type] = score

    best_match = max(scores, key=scores.get)

    return best_match if scores[best_match] > 0 else None

