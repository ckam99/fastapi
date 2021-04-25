

def unique_email():
    obj = await User.filter(Q(email=user.email) | Q(username=user.username)).first()
    return obj
    if obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exist')
