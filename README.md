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

ai_learning_platform/
├── app/
│   ├── __init__.py            # App factory
│   ├── routes/
│   │   └── api.py             # All API endpoints
│   ├── models/
│   │   └── models.py          # SQLAlchemy DB models
│   ├── services/
│   │   └── recommend.py       # Custom logic (e.g., recommendations)
│   └── utils/
│       └── helpers.py         # Utility functions
├── config.py                  # Config (DB, secret key, etc.)
├── requirements.txt           # Required Python packages
├── run.py                     # Entry point
└── README.md                  # This file


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
