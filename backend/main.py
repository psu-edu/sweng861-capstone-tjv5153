from datetime import datetime
from urllib import request
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import jwt
from okta_jwt.jwt import validate_token
from okta_jwt_verifier import BaseJWTVerifier
import os
import shutil
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import sqlite3
import ticketsDb_utils
import userDb_utils
import LicensePlateRecognitionAPI

load_dotenv()
OKTA_URL = os.getenv("OKTA_URL")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
BACKEND_URL = os.getenv("BACKEND_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")
USERS_DB_PATH = os.getenv("USERS_DB")
TICKETS_DB_PATH = os.getenv("TICKETS_DB")


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
origins = ["http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

templates = Jinja2Templates(directory="../frontend/templates")

# Fetch OpenID Connect metadata
metadata = httpx.get(f"{OKTA_URL}/.well-known/openid-configuration").json()
authorization_url = metadata["authorization_endpoint"]
token_url = metadata["token_endpoint"]

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    if request.url.path != "/revokeParkingPass" and request.url.path != "/addTicket" and request.url.path != "/removeTicket" \
    and request.url.path != "/checkTickets" and request.url.path != "/parkingPass":
        response = await call_next(request)
        print("No authentication required for this path")
        return response

    session_id = request.cookies.get("session_id")
    if not session_id:
        print("unauthorized1")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"Unauthorized": "Valid access token is required"}
        )
    else:
        is_valid = await validateTokens(session_id, "access_token")
        if not is_valid:
            print("unauthorized2")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"Unauthorized": "Invalid session Id"}
            )
        else:
            print("Session ID is valid")
            user_info = extractUserInfo(session_id)
            print(f"User Info from Middleware: {user_info}")

            #Attach user info to the request object for downstream use
            request.state.user = user_info['name']
            request.state.email = user_info['email']

            response = await call_next(request)
            return response

def verifyStatePostAuth(state: str):
    return state == "login"

def exchangeCodeForTokens(code: str):
    token_response = httpx.post(token_url,
    data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{BACKEND_URL}/authorization-code/callback",
            "client_id": OKTA_CLIENT_ID,
            "client_secret": OKTA_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if token_response.status_code != 200:
        print("Failed to exchange code for tokens")
        return None, None
    else:
        token_data = token_response.json()

        access_token = token_data.get("access_token")
        id_token = token_data.get("id_token")


        return access_token, id_token

async def validateTokens(token: str, token_type: str):
    jwt_verifier = BaseJWTVerifier(OKTA_URL, OKTA_CLIENT_ID, audience="api://default")

    try:
        if token_type == "id_token":
            await jwt_verifier.verify_id_token(token)
        elif token_type == "access_token":
            await jwt_verifier.verify_access_token(token)
        return True

    except Exception as e:
        print("Token validation failed:", str(e))
        return False
    
def extractUserInfo(token: str):
    print(token)
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    userinfo = {}
    userinfo['name'] = f'{decoded_token.get('name')} {decoded_token.get('lastName')}'
    userinfo['email'] = decoded_token.get('email')  
    userinfo['auth_time'] = decoded_token.get('auth_time')
    userinfo['iat'] = decoded_token.get('iat')
    userinfo['uid'] = decoded_token.get('uid')
    print(userinfo)

    return userinfo

async def isAuthenticated(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        print("No session ID found in cookies")
        return False
    else:
        is_valid = await validateTokens(session_id, "access_token")
        print("Verified using depends")
        return is_valid
    
async def isAuthenticated_officer(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return False
    else:
        is_valid = await validateTokens(session_id, "access_token")
        if not is_valid:
            return False
        else:
            user_info = extractUserInfo(session_id)
            return user_info['name'] in userDb_utils.OFFICERS_LIST

# Unprotected endpoints
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("../frontend/templates/favicon.ico")

@app.get("/health")
async def read_health():
    return {"status": "ok"}

@app.get("/signin")
async def signin():
    redirect_uri = f"{authorization_url}?client_id={OKTA_CLIENT_ID}&response_type=code&scope=openid&redirect_uri={BACKEND_URL}/authorization-code/callback&state=login"
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"redirect_uri": redirect_uri})

@app.get("/authorization-code/callback/")
async def authCallback(response: HTMLResponse, code:str, state:str):

    if(verifyStatePostAuth(state)):
        access_token, id_token = exchangeCodeForTokens(code)
  
        if(await validateTokens(access_token, "access_token") and await validateTokens(id_token, "id_token")):
            user_info = extractUserInfo(access_token)
            userDb_utils.addUsertoDB(user_info)
        else:
            print("Token validation failed")
            return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": "error", "message": "Token validation failed"})
    else:
        print("State verification failed")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": "error", "message": "State verification failed"})

    #update the redirect URL
    response = RedirectResponse(
        url=f"{FRONTEND_URL}/")

    response.set_cookie(
            key="session_id",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=36000
        )
    
    print("User authenticated and session cookie set")

    return response

#Protected endpoints, authentication required
@app.get("/checkTickets")
@limiter.limit("50/minute")
async def check_tickets(request: Request, licensePlate: str, verified: bool = Depends(isAuthenticated)):
    tickets = ticketsDb_utils.checkIfLicensePlateHasTicket(licensePlate)
    return JSONResponse(content={"tickets": tickets})

@app.get("/parkingPass")
@limiter.limit("50/minute")
async def get_parking_pass(request: Request, licensePlate: str, verified: bool = Depends(isAuthenticated)):
    if not verified:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    else:
        status = userDb_utils.addParkingPassToUser(licensePlate)
        if status:
            return JSONResponse(status_code=200, content={"message": "Parking pass added successfully"})
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to add parking pass"})

@app.post("/addTicket", response_model=ticketsDb_utils.Ticket)
@limiter.limit("50/minute")
async def add_ticket(request: Request, ticket:ticketsDb_utils.Ticket, verified: bool = Depends(isAuthenticated_officer)):
    if not verified:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    else:
        status = ticketsDb_utils.addTicket(ticket)
        if status:
            return JSONResponse(status_code=200, content={"message": "Ticket added successfully"})
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to add ticket"})

@app.delete("/removeTicket")
@limiter.limit("50/minute")
async def remove_ticket(request: Request, ticketId: int, verified: bool = Depends(isAuthenticated_officer)):
    if not verified:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    else:
        status = ticketsDb_utils.removeTicket(ticketId)
        if status:
            return JSONResponse(status_code=200, content={"message": "Ticket removed successfully"})
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to remove ticket"})

@app.put("/revokeParkingPass")
@limiter.limit("50/minute")
async def revoke_parking_pass(request: Request, licensePlate: str, verified: bool = Depends(isAuthenticated_officer)):
    if not verified:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    else:
        status = userDb_utils.removeParkingPassFromUser(licensePlate)
        if status:
            return JSONResponse(status_code=200, content={"message": "Parking pass revoked successfully"})
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to revoke parking pass"})

@app.post("/checkLicensePlate")
async def check_license_plate(file: UploadFile = File(...)):
    # Save the file locally
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = "demo.jpg" # use demo image for testing

    license_plate = LicensePlateRecognitionAPI.getLicensePlateFromImage(image)
    has_parking_pass = userDb_utils.checkIfUserHasParkingPass(license_plate)

    if has_parking_pass:
        return JSONResponse(status_code=200, content={"message": f"License plate {license_plate} has a valid parking pass"})
    else:
        return JSONResponse(status_code=403, content={"message": f"License plate {license_plate} does not have a valid parking pass"})


userDb_utils.setupUsersDb()
ticketsDb_utils.setupTicketsDb()
userDb_utils.print_all_users_database()
ticketsDb_utils.print_all_tickets_database()