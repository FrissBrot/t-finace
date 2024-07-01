import streamlit as st
import loginfunctions as lfn
import hashlib
import toastfunction as to

@st.experimental_dialog("Benutzerkonto löschen", width="large")
def popup_delete_user_account(user, session, cookie_manager):
    with st.form("delete user account"):
        st.write("Alle Benutzerdaten werden unwiderruflich gelöscht!")
        check = st.checkbox("Ich möchte mein Konto löschen.")
        submit = st.form_submit_button("Konto löschen")

        if submit:
            if check:
                st.session_state.user_id = None
                st.session_state.login = False
                lfn.del_useraccount(user)
                lfn.logoff(session)
                to.set_toast("Benutzerkonto wurde gelöscht", '✅')
                if "session_id" in cookie_manager.cookies:
                    cookie_manager.delete("session_id")
                st.rerun()

@st.experimental_dialog("Passwort ändern", width="large")
def popup_change_password(user, user_mail):
     with st.form("change password"):
            st.markdown("### Passwort ändern")
            password_to_verify = st.text_input("aktuelles Passwort *", placeholder = 'Aktuelles Passwort', type = 'password')
            password_new = st.text_input("Passwort *", placeholder = 'Neues Passwort', type = 'password')
            password_new_check = st.text_input("Passwort*", placeholder = 'Neues Passwort bestätigen', type = 'password')
            submitted_password_change = st.form_submit_button("Passwort ändern")
        
            if submitted_password_change:
                
                valid_new_password_check = lfn.check_valid_password(password_new, password_new_check)

                if valid_new_password_check == False:
                    st.error("Das Passwort ist nicht stark genug.")

                elif valid_new_password_check == None:
                    st.error("Die Passwörter stimmen nicht überein.")

                elif valid_new_password_check == True:

                    password_to_verify_hash = hashlib.sha256(password_to_verify.encode()).hexdigest()
                    password_new_hash = hashlib.sha256(password_new.encode()).hexdigest()
                    
                    if lfn.check_login(user_mail, password_to_verify_hash):
                        lfn.set_new_password(user, password_new_hash)
                        lfn.del_all_session(user)
                        to.set_toast("Passwort erfolgreich geändert", '✅')
                        st.rerun()

                    else:
                        st.error("Das aktuelle Passwort ist nicht korrekt.")

def SetLoginSessionState():
    cookie_manager = lfn.get_manager()
    session = cookie_manager.get(cookie="session_id")
    user = lfn.check_session(session)[1]

    LOGGED_IN = lfn.check_session(session)[0]
    if LOGGED_IN == True:
        #change st.session_state
        st.session_state.login = True
        st.session_state.user_id = user

def loadLogin():
    cookie_manager = lfn.get_manager()
    session_from_cookie = cookie_manager.get(cookie="session_id")

        #initialize sessions
    if 'login' not in st.session_state:
        st.session_state.login = False

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'state_session_id' not in st.session_state:
        st.session_state.state_session_id = None

    if session_from_cookie == None:
        session = st.session_state.state_session_id
    else:
        session = session_from_cookie

    user = lfn.check_session(session)[1]
    username = lfn.get_username(user)

    #user authentication
    LOGGED_IN = lfn.check_session(session)[0]
    print(LOGGED_IN)
    if LOGGED_IN == True:
        
        #change st.session_state
        st.session_state.login = True
        st.session_state.user_id = user

        #redirect when automatic Authentication
        if not st.session_state.redirect == None:
            page = st.session_state.redirect
            st.session_state.redirect = None
            print(page)
            #switch_page(page)

        user_mail = lfn.get_user_mail(user)

        st.header("Benutzerkonto")

        st.write("Dein Benutzername: {}".format(username))
        st.write("Deine Mailadresse: {}".format(user_mail))
        st.markdown("# ")
        if st.button("Abmelden"):
            lfn.logoff(session)
            if "session_id" in cookie_manager.cookies:
                cookie_manager.delete("session_id")
                to.set_toast("Abgemeldet", '✅')
            st.rerun()

        if st.button("von allen Geräten abmelden"):
            lfn.del_all_session(user)
            lfn.logoff(session)
            to.set_toast("Sie wurden überall abgemeldet.", '✅')
            if "session_id" in cookie_manager.cookies:
                cookie_manager.delete("session_id")
            st.rerun()

        if st.button("Passwort ändern"):
            popup_change_password(user, user_mail)
        
        st.markdown("# ")
        with st.form("Gefahrenzone"):
            st.markdown("### Gefahrenzone")
            st.markdown("# ")
            submit = st.form_submit_button("Benutzerkonto löschen")
            if submit:
                popup_delete_user_account(user, session, cookie_manager)

    else:
        st.session_state.login = False
        st.session_state.user_id = user
    
        tabLogin, tabRegister = st.tabs(["Login", "Registrieren"])

        with tabLogin:
            with st.form("Login"):
                st.markdown("### Anmelden")
                mail = st.text_input("E-Mailadresse oder Benutzername")
                password = st.text_input("Passwort", type="password")
                submitted_login = st.form_submit_button("Anmelden")
            

            if submitted_login:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                login_sucessful = lfn.check_login(mail, password_hash)
                
                if login_sucessful:
                    
                    #set session cookie
                    session_id = lfn.generate_session_id()
                    user_id = lfn.get_user_id(mail)
                    lfn.save_session_id(user_id, session_id)
                    if "session_id" in cookie_manager.cookies:
                        cookie_manager.delete("session_id")
                    cookie_manager.set("session_id", session_id)
                    
                    #set login state to st.session
                    st.session_state.login = True
                    st.session_state.user_id = user_id
                    st.session_state.state_session_id = session_id

                    #welcome message
                    message= ("Angemeldet als {}".format(mail))
                    to.set_toast(message, '✅')
                
                elif login_sucessful == False:
                    st.error("Benutzername oder Passwort ist falsch.")
                else:
                    st.error("Authentifizierungsfehler! Bitte wende dich an den Support.")

        with tabRegister:
            with st.form("Create User"):
                st.markdown("### Registrieren")
                email_sign_up = st.text_input("Email *", placeholder = 'Gibt deine E-Mailadresse an').lower()
                username_sign_up = st.text_input("Benutzername *", placeholder = 'Gib einen Benutzername an').lower()
                password_sign_up = st.text_input("Passwort *", placeholder = 'Erstelle ein starkes Passwort', type = 'password')
                password_sign_up_check = st.text_input("Passwort *", placeholder = 'Passwort bestätigen', type = 'password')
                terms_accept = st.checkbox("Ich akzepiere die Datenschutzerlkärung")
                submitted_register = st.form_submit_button("Benutzer erstellen")

            if submitted_register:

                valid_email_check = lfn.check_valid_email(email_sign_up)
                unique_email_check = lfn.check_unique_email(email_sign_up)
                valid_username_check = lfn.check_valid_username(username_sign_up)
                unique_username_check = lfn.check_unique_usr(username_sign_up)
                valid_password_check = lfn.check_valid_password(password_sign_up, password_sign_up_check)

                if valid_email_check == False:
                    st.error("Gib eine gültige E-Mailadresse an!")
                
                elif unique_email_check == False:
                    st.error("Die E-Mailadresse ist bereits registriert!")

                elif valid_username_check == False:
                    st.error("Der Beutzername ist ungültig!")
                
                elif unique_username_check == False:
                    st.error(f'Entschuldige, der Benutzername {username_sign_up} existiert bereits!')
                
                elif unique_username_check == None:
                    st.error('Benutzername darf nicht leer sein!')

                elif valid_password_check == None:
                    st.error("Passwörter stimmen nicht überein!")
                
                elif valid_password_check == False:
                    st.error("Das Passwort ist nicht strark genug!")
                
                elif terms_accept == False:
                    st.error("Bitte akzeptiere die Nutzungsbedingungen!")

                if valid_email_check == True:
                    if unique_email_check == True:
                        if valid_username_check == True:
                            if unique_username_check == True:
                                if terms_accept == True:
                                    if valid_password_check == True:
                                        lfn.register_new_usr(email_sign_up, username_sign_up, password_sign_up)
                                        to.set_toast("Registration erfolgreich!", '✅')

                                        #set session cookie
                                        session_id = lfn.generate_session_id()
                                        user_id = lfn.get_user_id(email_sign_up)
                                        lfn.save_session_id(user_id, session_id)
                                        if "session_id" in cookie_manager.cookies:
                                            cookie_manager.delete("session_id")
                                        cookie_manager.set("session_id", session_id)
                                        
                                        #set login state to st.session
                                        st.session_state.login = True
                                        st.session_state.user_id = user_id
                                        st.session_state.state_session_id = session_id