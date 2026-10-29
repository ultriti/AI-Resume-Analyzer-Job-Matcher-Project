import re
import spacy

SKILLS = {
    "Programming": {
        "python",
        "java",
        "c",
        "javascript",
        "sql",
    },
    "Machine Learning": {
        "machine learning",
        "scikit-learn",
        "feature engineering",
        "data preprocessing",
        "classification",
        "model evaluation",
        "random forest",
        "tf-idf",
    },
    "Deep Learning": {
        "deep learning",
        "tensorflow",
        "keras",
        "pytorch",
        "pytorch geometric",
        "pyg",
        "cnn",
        "cnns",
        "rnn",
        "rnns",
        "lstm",
        "gru",
        "bigru",
        "gcn",
        "neural networks",
        "transfer learning",
    },
    "Graph Machine Learning": {
        "graph neural network",
        "graph neural networks",
        "gnn",
        "graph convolutional network",
        "graph convolutional networks",
        "node classification",
        "citation networks",
        "graph representation learning",
        "message passing",
        "networkx",
    },
    "Natural Language Processing": {
        "natural language processing",
        "nlp",
        "text classification",
        "tokenization",
        "word embeddings",
        "sequence modeling",
        "nlp preprocessing",
        "hugging face",
        "tf-idf",
    },
    "Computer Vision": {
        "computer vision",
        "opencv",
        "image classification",
        "image processing",
        "emotion recognition",
        "facial emotion recognition",
    },
    "Generative AI & Agents": {
        "generative ai",
        "ai agents",
        "intent-based routing",
        "information retrieval",
        "ai task automation",
        "recommendation system",
    },
    "Data Science & Analytics": {
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "seaborn",
        "data preprocessing",
        "feature engineering",
        "statistical analysis",
        "probability estimation",
        "prediction",
    },
    "Backend & APIs": {
        "fastapi",
        "flask",
        "rest api",
        "rest apis",
        "pydantic",
        "onnx",
        "onnx runtime",
        "model serialization",
        "model inference",
        "web scraping",
        "beautifulsoup",
        "beautifulsoup4",
    },
    "Frontend Development": {
        "react",
        "react.js",
        "reactjs",
        "vite",
        "responsive design",
        "frontend development",
    },
    "Backend Development": {
        "node.js",
        "nodejs",
        "express.js",
        "expressjs",
        "backend development",
        "socket.io",
        "websockets",
    },
    "Full Stack Development": {
        "full stack development",
        "software development",
        "application development",
        "electron",
    },
    "Databases": {
        "sql",
        "postgresql",
        "mongodb",
    },
    "Tools & DevOps": {
        "git",
        "github",
        "jupyter notebook",
        "docker",
        "postman",
        "selenium",
        "api deployment",
        "model deployment",
        "cpu inference",
        "inference pipeline",
    },
    "Authentication & Cloud": {
        "jwt",
        "firebase",
        "cloudinary",
    },
    "Deep Learning Training Concepts": {
        "softmax",
        "cross entropy",
        "adam optimizer",
        "dropout",
        "early stopping",
        "checkpointing",
        "neural networks",
    },
    "Databases & Real-Time Systems": {
        "postgresql",
        "mongodb",
        "socket.io",
        "websockets",
    },
}

JOB_TITLES = [
    "ai/ml engineer",
    "machine learning engineer",
    "deep learning engineer",
    "nlp engineer",
    "computer vision engineer",
    "data scientist",
    "data analyst",
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "full stack engineer",
    "mern stack developer",
    "pern stack developer",
    "python developer",
    "research engineer",
    "ai engineer",
    "ml engineer",
]

JOB_TITLE_SKILL_MAP = {
    "ai/ml engineer": [
        "Programming & Software Engineering",
        "Data Structures & Algorithms",
        "Mathematics for AI",
        "Statistics & Probability",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision",
        "Generative AI",
        "LLMs & Prompt Engineering",
        "AI Agents & Agentic Systems",
        "Retrieval Augmented Generation (RAG)",
        "Vector Databases",
        "MLOps",
        "Data Engineering",
        "Cloud & Deployment",
        "Model Optimization",
        "Research & Experimentation",
    ],
    "machine learning engineer": [
        "Programming & Software Engineering",
        "Data Structures & Algorithms",
        "Mathematics",
        "Statistics & Probability",
        "Data Analysis",
        "Feature Engineering",
        "Machine Learning",
        "Model Evaluation",
        "Ensemble Methods",
        "Time Series Analysis",
        "MLOps",
        "Cloud Computing",
        "Model Deployment",
        "Databases",
    ],
    "deep learning engineer": [
        "Python Programming",
        "Linear Algebra",
        "Calculus",
        "Probability & Statistics",
        "Deep Learning Fundamentals",
        "Neural Networks",
        "CNNs",
        "RNNs & LSTMs",
        "Transformers",
        "Computer Vision",
        "NLP",
        "PyTorch",
        "TensorFlow",
        "Model Optimization",
        "Distributed Training",
    ],
    "nlp engineer": [
        "Python Programming",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "Text Processing",
        "Word Embeddings",
        "Transformers",
        "Large Language Models",
        "Prompt Engineering",
        "RAG Systems",
        "Vector Databases",
        "LangChain",
        "LlamaIndex",
        "Model Fine-Tuning",
        "Evaluation & Benchmarking",
    ],
    "computer vision engineer": [
        "Python Programming",
        "Machine Learning",
        "Deep Learning",
        "Image Processing",
        "OpenCV",
        "CNN Architectures",
        "Object Detection",
        "Segmentation",
        "OCR Systems",
        "Video Analytics",
        "Transformers for Vision",
        "PyTorch",
        "Model Deployment",
    ],
    "data scientist": [
        "Python Programming",
        "SQL",
        "Statistics",
        "Probability",
        "Data Cleaning",
        "Exploratory Data Analysis",
        "Data Visualization",
        "Machine Learning",
        "Feature Engineering",
        "A/B Testing",
        "Business Analytics",
        "Predictive Modeling",
        "Dashboarding",
    ],
    "data analyst": [
        "Excel",
        "SQL",
        "Python",
        "Data Cleaning",
        "Data Visualization",
        "Power BI",
        "Tableau",
        "Business Analytics",
        "Statistics",
        "Reporting & Dashboards",
    ],
    "software engineer": [
        "Programming",
        "Data Structures & Algorithms",
        "System Design",
        "Object Oriented Programming",
        "Databases",
        "Backend Development",
        "Frontend Development",
        "API Development",
        "Testing",
        "Git & GitHub",
        "DevOps",
        "Cloud Computing",
        "Security Fundamentals",
    ],
    "backend developer": [
        "Programming",
        "Data Structures & Algorithms",
        "Backend Development",
        "REST APIs",
        "GraphQL",
        "Databases",
        "Authentication & Authorization",
        "Microservices",
        "Caching",
        "Message Queues",
        "Cloud Deployment",
        "Docker",
        "CI/CD",
    ],
    "frontend developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "TypeScript",
        "React",
        "Next.js",
        "State Management",
        "Tailwind CSS",
        "Responsive Design",
        "Performance Optimization",
        "Testing",
        "Frontend Architecture",
    ],
    "full stack developer": [
        "Programming",
        "Frontend Development",
        "Backend Development",
        "Databases",
        "APIs",
        "Authentication",
        "System Design",
        "Cloud Computing",
        "Docker",
        "CI/CD",
        "Testing",
        "DevOps",
    ],
    "python developer": [
        "Python Fundamentals",
        "Object Oriented Programming",
        "Data Structures & Algorithms",
        "Backend Development",
        "FastAPI",
        "Django",
        "Flask",
        "REST APIs",
        "Databases",
        "Testing",
        "Docker",
        "Cloud Deployment",
    ],
    "research engineer": [
        "Programming",
        "Mathematics",
        "Probability & Statistics",
        "Machine Learning",
        "Deep Learning",
        "Research Methodology",
        "Paper Reading",
        "Experiment Tracking",
        "Model Development",
        "Scientific Writing",
        "MLOps",
    ],
    "ai engineer": [
        "Programming",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "Large Language Models",
        "Prompt Engineering",
        "RAG Systems",
        "AI Agents",
        "LangChain",
        "Vector Databases",
        "FastAPI",
        "Cloud Deployment",
        "MLOps",
        "System Design",
    ],
    "ml engineer": [
        "Programming",
        "Mathematics",
        "Statistics",
        "Machine Learning",
        "Feature Engineering",
        "Model Training",
        "Model Optimization",
        "MLOps",
        "Cloud Computing",
        "Data Engineering",
        "Databases",
    ],
}

SKILL_CATEGORY_MAP = {
    # =====================
    # Programming
    # =====================
    "python": "Programming",
    "java": "Programming",
    "c": "Programming",
    "javascript": "Programming",
    # =====================
    # Databases
    # =====================
    "sql": "Databases",
    "postgresql": "Databases",
    "mongodb": "Databases",
    # =====================
    # Machine Learning
    # =====================
    "machine learning": "Machine Learning",
    "scikit-learn": "Machine Learning",
    "classification": "Machine Learning",
    "random forest": "Machine Learning",
    "feature engineering": "Machine Learning",
    "model evaluation": "Machine Learning",
    "prediction": "Machine Learning",
    "data preprocessing": "Machine Learning",
    # =====================
    # Deep Learning
    # =====================
    "deep learning": "Deep Learning",
    "tensorflow": "Deep Learning",
    "keras": "Deep Learning",
    "pytorch": "Deep Learning",
    "cnn": "Deep Learning",
    "cnns": "Deep Learning",
    "rnn": "Deep Learning",
    "rnns": "Deep Learning",
    "lstm": "Deep Learning",
    "gru": "Deep Learning",
    "bigru": "Deep Learning",
    "neural networks": "Deep Learning",
    # =====================
    # Graph Machine Learning
    # =====================
    "graph neural network": "Graph Machine Learning",
    "graph neural networks": "Graph Machine Learning",
    "gnn": "Graph Machine Learning",
    "gcn": "Graph Machine Learning",
    "graph convolutional networks": "Graph Machine Learning",
    "node classification": "Graph Machine Learning",
    "message passing": "Graph Machine Learning",
    "networkx": "Graph Machine Learning",
    "citation networks": "Graph Machine Learning",
    "pyg": "Graph Machine Learning",
    "pytorch geometric": "Graph Machine Learning",
    # =====================
    # NLP
    # =====================
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "tokenization": "Natural Language Processing",
    "word embeddings": "Natural Language Processing",
    "text classification": "Natural Language Processing",
    "sequence modeling": "Natural Language Processing",
    "hugging face": "Natural Language Processing",
    "nlp preprocessing": "Natural Language Processing",
    "tf-idf": "Natural Language Processing",
    # =====================
    # Computer Vision
    # =====================
    "computer vision": "Computer Vision",
    "opencv": "Computer Vision",
    "image classification": "Computer Vision",
    "image processing": "Computer Vision",
    "emotion recognition": "Computer Vision",
    "facial emotion recognition": "Computer Vision",
    # =====================
    # Generative AI
    # =====================
    "generative ai": "Generative AI",
    "ai agents": "AI Agents",
    "intent-based routing": "AI Agents",
    "information retrieval": "RAG Systems",
    "recommendation system": "Generative AI",
    "ai task automation": "AI Agents",
    # =====================
    # Data Science
    # =====================
    "pandas": "Data Analysis",
    "numpy": "Data Analysis",
    "scipy": "Data Analysis",
    "matplotlib": "Data Visualization",
    "seaborn": "Data Visualization",
    # =====================
    # Backend Development
    # =====================
    "fastapi": "Backend Development",
    "flask": "Backend Development",
    "pydantic": "Backend Development",
    "rest api": "API Development",
    "rest apis": "API Development",
    # =====================
    # Backend / Node.js
    # =====================
    "node.js": "Backend Development",
    "express.js": "Backend Development",
    # =====================
    # Frontend Development
    # =====================
    "react": "Frontend Development",
    "react.js": "Frontend Development",
    "vite": "Frontend Development",
    # =====================
    # DevOps & Deployment
    # =====================
    "docker": "DevOps",
    "github": "Git & GitHub",
    "git": "Git & GitHub",
    "postman": "API Development",
    "model deployment": "Cloud Deployment",
    "inference pipeline": "Model Deployment",
    # =====================
    # Web Scraping
    # =====================
    "web scraping": "Data Engineering",
    "beautifulsoup": "Data Engineering",
    "selenium": "Data Engineering",
    # =====================
    # ONNX
    # =====================
    "onnx": "Model Deployment",
    "onnx runtime": "Model Deployment",
    "model serialization": "Model Deployment",
    "model inference": "Model Deployment",
    # =====================
    # Authentication
    # =====================
    "jwt": "Authentication",
    "firebase": "Authentication",
    "cloudinary": "Cloud Deployment",
    # =====================
    # Training Concepts
    # =====================
    "softmax": "Deep Learning",
    "dropout": "Deep Learning",
    "adam optimizer": "Deep Learning",
    "early stopping": "Deep Learning",
    "checkpointing": "Deep Learning",
    # =====================
    # Real-Time Systems
    # =====================
    "socket.io": "Backend Development",
}

ROLE_SKILL_CATEGORY_ALIASES = {
    "programming & software engineering": {"Programming"},
    "python programming": {"Programming"},
    "feature engineering": {"Machine Learning"},
    "ensemble methods": {"Machine Learning"},
    "time series analysis": {"Machine Learning"},
    "mathematics": {"Data Science & Analytics"},
    "mathematics for ai": {"Data Science & Analytics"},
    "statistics": {"Data Science & Analytics"},
    "statistics & probability": {"Data Science & Analytics"},
    "probability & statistics": {"Data Science & Analytics"},
    "data analysis": {"Data Science & Analytics"},
    "data cleaning": {"Data Science & Analytics"},
    "data visualization": {"Data Science & Analytics"},
    "business analytics": {"Data Science & Analytics"},
    "deep learning fundamentals": {"Deep Learning"},
    "neural networks": {"Deep Learning", "Deep Learning Training Concepts"},
    "cnns": {"Deep Learning"},
    "cnn architectures": {"Deep Learning", "Computer Vision"},
    "rnns & lstms": {"Deep Learning"},
    "pytorch": {"Deep Learning"},
    "tensorflow": {"Deep Learning"},
    "nlp": {"Natural Language Processing"},
    "text processing": {"Natural Language Processing"},
    "word embeddings": {"Natural Language Processing"},
    "image processing": {"Computer Vision"},
    "opencv": {"Computer Vision"},
    "programming": {"Programming"},
    "api development": {"Backend & APIs"},
    "rest apis": {"Backend & APIs"},
    "apis": {"Backend & APIs"},
    "git & github": {"Tools & DevOps"},
    "devops": {"Tools & DevOps"},
    "docker": {"Tools & DevOps"},
    "cloud deployment": {"Authentication & Cloud", "Tools & DevOps"},
    "cloud & deployment": {"Authentication & Cloud", "Tools & DevOps"},
}


# -------------------------------------------------------------------
# Corrected extraction utilities
# -------------------------------------------------------------------

# Canonicalize aliases before returning skills so duplicate variants
# such as React.js / ReactJS and GNN / graph neural network don't inflate
# the extracted skill list.
SKILL_ALIASES = {
    "python3": "python",
    "js": "javascript",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "react.js": "react",
    "reactjs": "react",
    "nodejs": "node.js",
    "expressjs": "express.js",
    "pyg": "pytorch geometric",
    "gnn": "graph neural network",
    "graph neural networks": "graph neural network",
    "gcn": "graph convolutional network",
    "graph convolutional networks": "graph convolutional network",
    "cnns": "cnn",
    "rnns": "rnn",
    "rest apis": "rest api",
    "beautifulsoup4": "beautifulsoup",
    "huggingface": "hugging face",
    "postgres": "postgresql",
    "web sockets": "websockets",
    "llms": "large language models",
    "rag": "retrieval augmented generation",
}


def normalize_skill(skill):
    """Normalize a skill label without destroying meaningful symbols."""
    skill = str(skill).lower().strip()
    skill = skill.replace("&", " and ")
    skill = re.sub(r"\s+", " ", skill).strip()
    return SKILL_ALIASES.get(skill, skill)


def _skill_pattern(skill):
    """
    Build a phrase-aware pattern.
    Allows punctuation in skill names such as C++, Node.js and TF-IDF.
    """
    escaped = re.escape(skill.strip())
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(
        rf"(?<![\w+#]){escaped}(?![\w+#])",
        flags=re.IGNORECASE,
    )


def extract_titles(resume_text):
    """Extract job titles explicitly mentioned in the resume text."""
    text = str(resume_text or "")
    matched_titles = []

    # Longer titles first helps avoid partial overlaps.
    for title in sorted(JOB_TITLES, key=len, reverse=True):
        if _skill_pattern(title).search(text):
            matched_titles.append(title)

    return matched_titles


def extract_skills_loop(text, job_role=None):
    """
    Extract every recognized skill from resume text.

    `job_role` is accepted for backward compatibility, but deliberately
    does not filter extraction. Filtering by role categories previously
    discarded skills because requirement names and SKILLS category names
    are different vocabularies. Compare extracted skills to the selected
    role's requirements after extraction instead.
    """
    text = str(text or "")
    found_skills = set()

    # Longest phrases first. Set-based output removes duplicate matches.
    all_skills = {
        skill
        for category_skills in SKILLS.values()
        for skill in category_skills
    }

    for skill in sorted(all_skills, key=len, reverse=True):
        if _skill_pattern(skill).search(text):
            found_skills.add(normalize_skill(skill))

    # Return stable output for predictable API responses and tests.
    return sorted(found_skills)


def extract_skills_spacy(text):
    """
    Return spaCy named entities, NOT skills.

    General spaCy NER labels usually do not identify technical skills.
    Use extract_skills_loop() for skills recognized by the SKILLS
    vocabulary. This function is retained for compatibility.
    """
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print(
            "SpaCy model 'en_core_web_sm' not found. "
            "Install it with: python -m spacy download en_core_web_sm"
        )
        return []

    doc = nlp(str(text or ""))
    return [(ent.text, ent.label_) for ent in doc.ents]
