from flask import Flask, request, jsonify
import requests
import json
import os
from urllib.parse import urljoin, urlparse
import time

app = Flask(__name__)

# Gemini AI Configuration
GEMINI_API_KEY = "AIzaSyCjSyc6BFhPoHxPrI8e4eH6FjPv8D8Qx2g"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-002:generateContent"

# CS Self-Study Guide main pages and content
CS_GUIDE_CONTENT = {
    "programming_languages": {
        "Python": "Beginner-friendly, concise syntax, widely applicable",
        "Java": "Object-oriented programming, commonly used in enterprise development",
        "C/C++": "System programming, high-performance scenarios",
        "JavaScript": "Essential for frontend development, also used for backend",
        "Go": "Modern system programming language, excellent concurrency performance"
    },
    "computer_science_fundamentals": {
        "Data Structures and Algorithms": "Programming foundation, essential for interviews",
        "Computer Systems": "Deep understanding of how computers work",
        "Operating Systems": "Essential knowledge for system-level programming",
        "Computer Networks": "Foundation for network programming and distributed systems",
        "Databases": "Data storage and management"
    },
    "specialized_fields": {
        "Machine Learning": "AI field entry, high math requirements",
        "Frontend Development": "User interface development, highly creative",
        "Backend Development": "Server-side development, highly logical",
        "Mobile Development": "iOS/Android app development",
        "Game Development": "Game engines and graphics programming"
    },
    "tools_and_platforms": {
        "Git": "Version control, essential for team collaboration",
        "Linux": "Development environment, server operations",
        "Docker": "Containerization technology, deployment tool",
        "AWS/Cloud Services": "Modern application deployment and operations"
    }
}

def get_gemini_response(prompt, context=""):
    """Call Gemini AI API with retry mechanism"""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY environment variable not set"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Shorter, more focused prompt to reduce token usage
    full_prompt = f"""
    You are a CS learning advisor based on CS Self-Study Guide (https://csdiy.wiki/).
    
    User question: {prompt}
    
    Provide concise advice on:
    1. Learning path
    2. Key resources
    3. Practice projects
    
    Keep response under 300 words.
    """
    
    data = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }]
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "Sorry, no valid response was obtained."
            elif response.status_code == 429:
                # Rate limit exceeded
                error_data = response.json()
                if attempt < max_retries - 1:
                    # Wait and retry
                    wait_time = min(60, 2 ** attempt * 10)  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                else:
                    return get_fallback_response(prompt)
            else:
                return f"API call failed: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return get_fallback_response(prompt)
        except Exception as e:
            return f"Processing error: {str(e)}"
    
    return get_fallback_response(prompt)

def get_fallback_response(prompt):
    """Provide fallback response when API is unavailable"""
    prompt_lower = prompt.lower()
    
    # Basic keyword matching for common questions
    if any(word in prompt_lower for word in ['beginner', 'start', 'first', 'new']):
        return """
        **Getting Started with Programming:**
        
        1. **Start with Python** - Easy syntax, great for beginners
        2. **Learn fundamentals** - Variables, loops, functions, data structures
        3. **Practice daily** - Solve problems on LeetCode, HackerRank
        4. **Build projects** - Calculator, to-do list, simple games
        
        **Resources:**
        - Python.org tutorial
        - Automate the Boring Stuff with Python
        - CS50 Introduction to Computer Science
        
        **Next steps:** Once comfortable with Python, explore web development (HTML/CSS/JavaScript) or data structures & algorithms.
        """
    
    elif any(word in prompt_lower for word in ['web', 'frontend', 'backend', 'fullstack']):
        return """
        **Web Development Path:**
        
        1. **Frontend basics** - HTML, CSS, JavaScript
        2. **Frontend framework** - React or Vue.js
        3. **Backend basics** - Node.js or Python Flask/Django
        4. **Database** - SQL basics, PostgreSQL or MongoDB
        5. **DevOps basics** - Git, deployment, basic AWS
        
        **Projects to build:**
        - Portfolio website
        - Todo app with backend
        - E-commerce site
        - Blog platform
        
        **Timeline:** 6-12 months with consistent practice (2-3 hours/day)
        """
    
    elif any(word in prompt_lower for word in ['machine learning', 'ai', 'data science']):
        return """
        **Machine Learning Path:**
        
        1. **Math prerequisites** - Linear algebra, statistics, calculus basics
        2. **Python for ML** - NumPy, Pandas, Matplotlib
        3. **ML fundamentals** - Supervised/unsupervised learning
        4. **Frameworks** - Scikit-learn, then TensorFlow or PyTorch
        
        **Resources:**
        - Andrew Ng's ML Course
        - Hands-On Machine Learning book
        - Kaggle competitions
        
        **Projects:** Iris classification, house price prediction, image recognition
        """
    
    else:
        return """
        **General CS Learning Advice:**
        
        1. **Foundations first** - Pick one programming language, master the basics
        2. **Practice regularly** - Code every day, even if just 30 minutes
        3. **Build projects** - Apply what you learn in real projects
        4. **Join communities** - GitHub, Stack Overflow, Reddit r/programming
        
        **Core topics to cover:**
        - Data structures & algorithms
        - System design basics
        - Version control (Git)
        - One specialization (web dev, mobile, ML, etc.)
        
        Sorry, our AI service is temporarily unavailable. This is a basic response based on common CS learning patterns.
        """

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """API endpoint for getting learning recommendations"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Please provide question parameter'
            }), 400
        
        question = data['question']
        context = data.get('context', '')
        
        # Call Gemini AI
        recommendation = get_gemini_response(question, context)
        
        return jsonify({
            'question': question,
            'recommendation': recommendation,
            'source': 'CS Self-Study Guide (https://csdiy.wiki/)',
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error occurred while processing request: {str(e)}'
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get main categories of CS learning"""
    return jsonify({
        'categories': CS_GUIDE_CONTENT,
        'description': 'Main learning categories based on CS Self-Study Guide'
    })

@app.route('/api/quick-start', methods=['POST'])
def quick_start():
    """Quick start suggestions"""
    try:
        data = request.get_json()
        background = data.get('background', 'Complete beginner')
        interest = data.get('interest', 'Uncertain')
        time_commitment = data.get('time_commitment', '1-2 hours per day')
        
        prompt = f"""
        User background: {background}
        Interest direction: {interest}
        Time commitment: {time_commitment}
        
        Please create a detailed CS learning entry plan for this user.
        """
        
        recommendation = get_gemini_response(prompt)
        
        return jsonify({
            'user_profile': {
                'background': background,
                'interest': interest,
                'time_commitment': time_commitment
            },
            'learning_plan': recommendation,
            'source': 'CS Self-Study Guide Personalized Recommendations'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error occurred while generating learning plan: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CS Self-Study Guide Recommendation API',
        'gemini_configured': bool(GEMINI_API_KEY)
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation homepage"""
    return jsonify({
        'name': 'CS Self-Study Guide Recommendation API',
        'description': 'Based on CS Self-Study Guide website content, using Gemini AI to provide personalized learning recommendations',
        'endpoints': {
            'POST /api/recommend': 'Get learning recommendations',
            'GET /api/categories': 'Get learning categories',
            'POST /api/quick-start': 'Quick start suggestions',
            'GET /health': 'Health check'
        },
        'usage': {
            'recommend': {
                'method': 'POST',
                'body': {
                    'question': 'Your question',
                    'context': 'Optional context information'
                }
            },
            'quick_start': {
                'method': 'POST', 
                'body': {
                    'background': 'Your background',
                    'interest': 'Interest direction',
                    'time_commitment': 'Time commitment'
                }
            }
        }
    })

if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY environment variable not set")
        print("Please set environment variable: export GEMINI_API_KEY='your_api_key_here'")
    
    app.run(port=5002, debug=True)