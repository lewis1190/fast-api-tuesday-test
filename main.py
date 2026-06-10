from fastapi import FastAPI, HTTPException, status, Depends

from dtos.login_dto import LoginDTO
from firebase.firebase import get_data, db
from firebase.auth import get_current_user

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/login")
def login(login_dto: LoginDTO):
    # This is a placeholder for actual authentication logic
    print(
        f"Received login attempt for username: {login_dto.username}, password: {login_dto.password}")
    if login_dto.username == "admin" and login_dto.password == "password":
        print("Login successful")
        return {"message": "Login successful"}
    else:
        print("Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")


@app.get("/data")
def get_data_endpoint(current_user: dict = Depends(get_current_user)):
    """Retrieve all data from Firestore (requires Firebase auth)"""
    return get_data("data")


@app.post("/seed")
def seed():
    """Seed the database with 3 initial data items"""
    sample_data = [
        {"name": "Item 1", "description": "This is item 1"},
        {"name": "Item 2", "description": "This is item 2"},
        {"name": "Item 3", "description": "This is item 3"},
    ]

    for data in sample_data:
        db.collection("data").add(data)

    return {"message": f"Seeded {len(sample_data)} items into Firestore"}
