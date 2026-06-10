from fastapi import HTTPException, status, Request

from firebase.firebase import verify_token


def get_current_user(request: Request):
    """Dependency to verify Firebase bearer token"""
    auth_header = request.headers.get("authorization")
    
    if not auth_header:
        print("No authorization header provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")
        
        decoded_token = verify_token(token)
        return decoded_token
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
