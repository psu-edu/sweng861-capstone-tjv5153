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
`cd backend`  
`uvicorn main:app --reload`  
Backend runs on port 8000

---

**Running Frontend**  
`cd frontend/react-app`  
`npm run dev`  
Frontend runs on port 5173

---
