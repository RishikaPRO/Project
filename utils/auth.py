USERS={
    "manager":{"password":"manager123","role":"Reporting Manager","team":"AD_Tools Team"},
    "srm":{"password":"srm123","role":"Reporting Manager","team":"AD_Tools Team"},
    "rish123":{"password":"rishika123","role":"Team Member","team":"AD_Tools Team"},
    "rish":{"password":"rishika123","role":"Reporting Manager","team":"AD_Tools Team"},


}
def authenticate(username,password):
    user=USERS.get(username.lower())
    if user and user["password"]==password:
        return user
    return False