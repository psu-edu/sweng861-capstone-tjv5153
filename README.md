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
OKTA_URL=https://integrator-7714547.okta.com/oauth2/default  
OKTA_CLIENT_ID=0oazhe55z0YsOjWHn697  
OKTA_CLIENT_SECRET=opCPfpAe0RCjSuqChiwFtT_XvqBCsGREOtBj-f8eNrHr3HY98yG_h0Fi9nppKjPn  
BACKEND_URL=http://localhost:8000  
FRONTEND_URL=http://localhost:5173  
USERS_DB=../database/users.db  
TICKETS_DB=../database/tickets.db  
TEST_TOKEN=eyJraWQiOiJRVWhKU3pTWXBxSlpmRHhKV0liM0I1OHdGMi1EMC1Dby1PSEt6aTZTa1o0IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmVTUUM1QjU0RjdHb19mVXJoNHVEUi12SWRzamliM3JIYng1anBWZHc3OGMiLCJpc3MiOiJodHRwczovL2ludGVncmF0b3ItNzcxNDU0Ny5va3RhLmNvbS9vYXV0aDIvZGVmYXVsdCIsImF1ZCI6ImFwaTovL2RlZmF1bHQiLCJpYXQiOjE3NzExMTU0MzYsImV4cCI6MTc3MTExOTAzNiwiY2lkIjoiMG9hemhlNTV6MFlzT2pXSG42OTciLCJ1aWQiOiIwMHV6aDZhOTR4eFBnc0FsYjY5NyIsInNjcCI6WyJvcGVuaWQiXSwiYXV0aF90aW1lIjoxNzcxMTE1NDM0LCJzdWIiOiJ0anY1MTUzQHBzdS5lZHUiLCJsYXN0TmFtZSI6IlZvbGthciIsIm5hbWUiOiJUaW0iLCJlbWFpbCI6InRqdjUxNTNAcHN1LmVkdSJ9.mU34aBKBHjxht9qM9qJY_J4hAPnUUb0Zz8ybvJdo0aVE1T6H7cpa806XyrdSRnyXlpN_4auOv8ZllSzgWWY0BGgQijdlWS-jeOeqh8EjXHk5_jY2qF3aaduZs5oZ7NiBdWd1MNGydhBb2wVDYNg4JjL8qM45I74aMRBPeMq_8gIQb79LYeIaMUeLAhHRjeveWXZynZgvTeGep7UUYKiVwZshQcpZsCUTaegDq8413aSB5cfArZ_N-6pyHKoL4D87tneVBak3zyGN8deoGYBkK6GqZVash8zvtz5NebMYEXCn8XnKCn2csTxpGTwWbMGGyBr1_3VJctUSd6S-xzJirQ  
OFFICERS='["Tim Volkar", "John", "Sarah", "Emily", "Michael"]'  
API_TOKEN=6cffe98f4fbb0df0bc97d2a6206f9f061729d218  