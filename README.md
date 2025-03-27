# LeanLens

**LeanLens** is a web-based AI fitness coach powered by Azure OpenAI and Computer Vision. Upload a photo of yourself and get a personalized body fat analysis and fat-loss plan.

## 🔍 What It Does

- Estimates current body fat % based on image analysis
- Uses Azure Vision to extract tags from uploaded photos
- Feeds tags to GPT to interpret and estimate body composition
- Generates a personalized plan using GPT-4 with:
  - Caloric intake & macros
  - Weekly workout schedule
  - Timeline to goal
  - Motivational tips

## 🧰 Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Backend:** Flask (Python)
- **AI Services:** Azure OpenAI + Azure Computer Vision

## 🚀 How to Run Locally

1. Clone this repo
2. Replace API keys and endpoints in `generate_plan.py`
3. Start backend:
    ```bash
    python generate_plan.py
    ```
4. Open `index.html` in your browser

## 📦 Dependencies

- Flask
- Flask-CORS
- Requests
- OpenAI SDK (`openai>=1.0`)

## 🔐 Environment Setup

Make sure to set your Azure keys securely. Do not commit them to version control.

## 📄 License

MIT License
