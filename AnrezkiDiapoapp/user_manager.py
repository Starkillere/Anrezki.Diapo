from hashlib import sha1

def add_user(password, acce, table, db):
    hashedPassword = sha1(password.encode()).hexdigest()
    user = table(hashedPassword, acce)
    db.session.add(user)
    db.session.commit()

def login(password, table):
    hashedPassword = sha1(password.encode()).hexdigest()
    user = table.query.filter_by(password=hashedPassword).first()
    if user != None:
        return user.droit_acces
    return False