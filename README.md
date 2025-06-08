# 🧠 AI Learning Platform Backend

A simple Flask-based backend for managing AI learning resources, user learning paths, and personalized roadmap recommendations.

## 🚀 Features

- Get all available learning tracks (Web, Data, etc.)
- View multi-stage roadmap for each track
- Personalized path recommendation
- Learning resource search
- User progress management
- Feedback collection
- User login and basic authentication

## 📁 Project Structure

your_project/
│
├── app/                        
│   ├── __init__.py             
│   ├── models/                 
│   │   ├── __init__.py
│   │   ├── user.py            
│   │   ├── track.py            
│   │   ├── resource.py         
│   │   └── progress.py         
│   │
│   ├── routes/                 
│   │   ├── __init__.py
│   │   ├── track_routes.py     
│   │   ├── user_routes.py      
│   │   ├── resource_routes.py  
│   │   └── feedback_routes.py  
│   │
│   ├── services/              
│   │   └── recommendation.py   
│   │
│   ├── utils/                  
│   │   └── helpers.py
│   │
│   └── config.py               
│
├── run.py                     
├── requirements.txt            
└── README.md

# 📦 API Endpoints

| Endpoint                     | Method | Description                  |
|------------------------------|--------|------------------------------|
| `/tracks`                    | GET    | Get all learning tracks      |
| `/roadmap/<track_id>`        | GET    | Get staged roadmap for a track |
| `/recommend-path`            | POST   | Recommend a personalized path |
| `/resources/search`          | GET    | Search resources             |
| `/user/<user_id>/progress`   | GET    | Get user progress            |
| `/user/<user_id>/progress/update` | POST | Update user progress       |
| `/feedback`                  | POST   | Submit feedback             |
| `/resources/all`             | GET    | Get all resources (admin)   |
| `/login`                    | POST   | Basic user login             |
