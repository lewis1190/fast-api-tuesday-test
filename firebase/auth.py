from fastapi import HTTPException, status, Depends, Request

from firebase.firebase import verify_token


def get_current_user(request: Request):
    """Dependency to verify Firebase bearer token"""
    auth_header = request.headers.get("authorization")
    print(f"Auth header: {auth_header}")
    
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
        
        print(f"Verifying token: {token}")
        decoded_token = verify_token(token)
        print(f"Authenticated user: {decoded_token['uid']}")
        return decoded_token
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
