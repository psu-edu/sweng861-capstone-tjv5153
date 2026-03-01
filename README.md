# sweng861-capstone-tjv5153

**Tim Volkar**  
**SWENG 861**  
**Campus Transit**  
This project is an application that streamlines campus parking for commuter students. Parking permits can be purchased using this application and enforcement officers can issue tickets. It will also provide access to the campus parking garage using license plates.

---

**Tech Stack:**

- Backend: Python FastAPI
- Frontend: React
- Database: SQL using SQLite

---

# Authentication Strategy

**Option C: Enterprise SSO**  
This option was chosen because the Campus Transit project is an internal tool that will be used by enforcement officers and students. Using enterprise SSO for internal tools streamlines the login process for a better user experience. Additionally, this keeps the application secure by utilizing the same policies as the rest of the organization.

---

**Running Backend**  
- Install on dependencies in backend/requirements.txt
`pip install -r requirements.txt`
`cd backend`  
`uvicorn main:app --reload`  
Backend runs on port 8000  
http://localhost:8000    

---

**Running Frontend**  
`cd frontend/react-app`  
`npm run dev`  
Frontend runs on port 5173
http://localhost:5173  

---
**Running Tests**  
Backend:
`cd backend`    
`pytest tests/ --cov=. --cov-report html`  
-s shows prints in the console  
--cov and --cov-report html generate a coverage report in html
Open tests\htmlcov\index.html in a browser to view the backend coverage report  
Frontend:  
`cd frontend/react-app`  
`npm run test`  
`npm run test:coverage` for coverage report  
Open frontend\react-app\coverage\index.html in a browser to view the frontend coverage report

---

**Building Docker Images**  
Backend:  
`docker build -t backend .`  
`docker run -p 8000:8000 --env-file .env backend`  
Frontend:  
`cd frontend`  
`docker build -t frontend .`  
`docker run -p 5173:5173 frontend`

---

**Environment Variables**  
**Example .env file**  
OKTA_URL=https://integrator-7714547.okta.com/oauth2/default  
OKTA_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXX  
OKTA_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXX  
BACKEND_URL=http://localhost:8000  
FRONTEND_URL=http://localhost:5173  
USERS_DB=../database/users.db  
TICKETS_DB=../database/tickets.db  
TEST_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXX  
OFFICERS='["Tim Volkar", "John", "Sarah", "Emily", "Michael"]'  
API_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXX  

---