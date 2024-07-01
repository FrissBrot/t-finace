# function for user login
# Timo Weber - Mai 2024

from pathlib import Path
import dbfunctions as db
import extra_streamlit_components as stx
import secrets
import string
import re
import hashlib
import random
import streamlit as st
from datetime import datetime, timedelta

# Function for loading the content from a text file (eg. Markdown, plain text, HTML)
def readFileContent(file):
    content = Path(file).read_text()
    return content

#cookie manager
def get_manager():
    return stx.CookieManager()

#generate session ids for user login
def generate_session_id(length=32):
    alphabet = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(alphabet) for _ in range(length))
    return session_id

#random code for password reset
def generate_random_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=8))
    return code


#save session id in db
def save_session_id(user, session_id):
    params = session_id, user
    query = (('INSERT INTO public."session" ("token", "fk_user") VALUES (\'%s\', %s);') % params)
    db.executeWithoutFetch(query)

#save code for password reset to db
def set_recode_to_db(recode, user_id):
        current_time = datetime.now()
        expiration_time = current_time + timedelta(minutes=10)

        params = recode, expiration_time, user_id
        query = (('UPDATE public."user" SET resetcode = \'%s\', codevaliduntil = \'%s\' WHERE id = \'%s\';') % params)
        db.executeWithoutFetch(query)

#check the code for passwordreset
def check_recode(recode, user_id):
        current_time = datetime.now()

        params = recode, user_id
        query = (('SELECT "codevaliduntil" FROM public."user" WHERE "resetcode" = \'%s\' AND id = \'%s\';') % params)
        print(query)
        answer = db.executeQuery(query)
        print(answer)
        if len(answer) > 0:
            if current_time <= answer[0][0]:
                return True
            else: return False
        else: return None

def del_recode(user_id):
        params = user_id
        query = (('UPDATE public."user" SET resetcode = NULL, codevaliduntil = NULL WHERE id = \'%s\';') % params)
        db.executeWithoutFetch(query)

#get user_id from mail or username
def get_user_id(user_unique_attribute):
    params = (user_unique_attribute, user_unique_attribute)
    query = (('SELECT id FROM public."user" WHERE (mail = \'%s\' OR username = \'%s\') AND active = True;') % params)
    answer = db.executeQuery(query)
    print(answer)
    print(len(answer))
    if len(answer) == 1:
        print("JAAAAAAAA")
        return answer[0][0]
    else:
        print("Neiiiiii") 
        return None

#get mail from user id
def get_user_mail(user_id):
        query = (('SELECT mail FROM public."user" WHERE id = \'%s\' AND active = True;') % user_id)
        answer = db.executeQuery(query)
        return answer[0][0]

def check_login(user_unique_attribute, passwordhash):
    params = (user_unique_attribute.lower(), passwordhash, user_unique_attribute.lower(), passwordhash)
    query = (('SELECT id FROM public."user" WHERE ((mail = \'%s\' AND password = \'%s\') OR (username = \'%s\' AND password = \'%s\') AND active = True);') % params)
    answer = db.executeQuery(query)
    if len(answer) == 0:
        return False
    elif len(answer) == 1:
        #set session cookie
        return True
    else:
        return None


def del_all_session(user_id):
    query = (('DELETE FROM public."session" WHERE user_id = \'%s\';') % user_id)
    db.executeWithoutFetch(query)

def del_all_user_dayplan(user_id):
    queryDayplans = 'SELECT "id" FROM "dayplan" WHERE "user_id" = %i;' % (user_id)
    userDayplansDB = db.executeQuery(queryDayplans)
    if len(userDayplansDB) > 0:
        userDayplanID = userDayplansDB[0][0]
        query = (('DELETE FROM "ZT_dayplan_attractions" WHERE "dayplan_id" = \'%s\';') % userDayplanID)
        db.executeWithoutFetch(query)

    query = (('DELETE FROM public."dayplan" WHERE user_id = \'%s\';') % user_id)
    db.executeWithoutFetch(query)

def del_useraccount(user_id):
    del_all_session(user_id)
    del_all_user_dayplan(user_id)
    query = (('DELETE FROM public."user" WHERE id = \'%s\';') % user_id)
    db.executeWithoutFetch(query)

def set_new_password(user_id, password_hash):
    params = password_hash, user_id
    query = (('UPDATE public."user" SET password = \'%s\' WHERE id = \'%s\';') % params)
    db.executeWithoutFetch(query)

def check_session(session_id):
    if st.session_state.login == True:
        return True, st.session_state.user_id
    else:
        query = ('SELECT public."user".id FROM session JOIN public."user" ON public."user".id = session.fk_user WHERE session.token = \'%s\' AND active = True;' % session_id)
        answer = db.executeQuery(query)
        if len(answer) == 0:
            return False, None
        else: return True, answer[0][0]

def get_username(user_id):
    if user_id == None:
        return None
    query = (('SELECT username FROM public."user" WHERE id = %s;') % user_id)
    answer = db.executeQuery(query)
    return answer[0][0]

def logoff(session):
    query = (('DELETE FROM public."session" WHERE token = \'%s\';') % session)
    db.executeWithoutFetch(query)
    st.session_state.user_id = None
    st.session_state.state_session_id = None
    st.session_state.login = False

def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False

def check_valid_password(password_sign_up, password_sign_up_check):
    """
    Checks if the two Passwords are the same.
    """
    if (password_sign_up == password_sign_up_check):
        if len(password_sign_up) < 8:
            return False
        # Überprüfen, ob das Passwort mindestens eine Großbuchstaben, Kleinbuchstaben, Zahl und Sonderzeichen enthält
        if not re.search(r"[A-Z]", password_sign_up):
            return False
        if not re.search(r"[a-z]", password_sign_up):
            return False
        if not re.search(r"[0-9]", password_sign_up):
            return False
        if not re.search(r"[!@#$%^&*()_+{}:;.,?]", password_sign_up):
            return False
        
        return True
    else:
            return None

def check_valid_username(username):
    pattern = r'^[a-z0-9]+$'

    # Match the pattern with the username
    if re.match(pattern, username.lower()):
        return True
    else:
        return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    query = (('SELECT id FROM public."user" WHERE mail = \'%s\';') % email_sign_up.lower())
    answer = db.executeQuery(query)
    if len(answer) == 0:
        return True
    else: return False

def check_unique_usr(email_usr: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    query = (('SELECT id FROM public."user" WHERE username = \'%s\';') % email_usr.lower())
    answer = db.executeQuery(query)

    if len(answer) == 0:
        return True
    else: return False

def register_new_usr(email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """

    password_hash = hashlib.sha256(password_sign_up.encode()).hexdigest()

    query = ('INSERT INTO "user" ("username", "mail", "password", "active") VALUES (\'%s\', \'%s\', \'%s\', true)'% (username_sign_up.lower(), email_sign_up.lower(), password_hash))
    db.executeWithoutFetch(query)