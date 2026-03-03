from fastapi import Header, HTTPException


def verify_admin(x_role: str = Header(...)):
    # Client must send:  X-Role: admin
    if x_role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Only admin can perform this action")