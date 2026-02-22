# RescueRoute — AI Food Rescue & Redistribution (PoC)

One-liner: Detect surplus food and optimally match & route pickups to verified NGOs.

## How to run (local)

### Backend
```bash
cd backend
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
Frontend
cd frontend
npm install
npm run dev
# open http://127.0.0.1:5173
Demo
•	Upload an image and text like: 30 meals cooked 2 hours ago lat:11.02 lng:76.95
•	Click Analyze and Show Optimized Route.
TRL claim
TRL-3: integrated PoC demonstrating end-to-end behavior with sample partners.
Contact
Team RescueRoute — <Lalit Kishore Alias Ashwanth Krishna KP \ iamashwanthkrishna@gmail.com  >

### Commit & push 

1. Go to :contentReference[oaicite:2]{index=2} website, log in, create a new repository named `RescueRoute` (choose Public or Private).
2. Follow the instructions they show. In your terminal (project root):
```bash
git add .
git commit -m "Initial RescueRoute PoC"
# replace <your-github-url> with the GitHub repo clone URL
git remote add origin <your-github-url>
git branch -M main
git push -u origin main
