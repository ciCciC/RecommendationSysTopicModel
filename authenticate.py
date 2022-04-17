import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd


def authenticate():
    # 0. Load users
    df_users = pd.read_csv('./data/fake_users.csv').iloc[:3]

    # 1. retrieve user credentials
    user_names = df_users.username.tolist()
    names = user_names
    passwords = ['123', '456', '358']

    # 2. create a hash for each passwords so that we do not send these in the clear
    hashed_passwords = stauth.Hasher(passwords).generate()

    # 3. create the authenticator which will create an authentication session cookie with an expiry interval
    authenticator = stauth.Authenticate(names, names, hashed_passwords, 'streamlit-auth-0', 'streamlit-auth-0-key',cookie_expiry_days=1)
    # 4. display the login form in the sidebar
    st.caption('user name: Roolearm')
    st.caption('password: 358')
    name, authentication_status, username = authenticator.login('Login','sidebar')

    # 5. the streamlit_authenticator library keeps state of the authentication status in streamlit's st.session_state['authentication_status']

    # > if the authentication succeeded (i.e. st.session_state['authentication_status'] == True)
    if st.session_state['authentication_status']:
        # display name on the sidebar
        with st.sidebar:
            st.text(username)

        # set user id in session state
        user_id = int(df_users[df_users['username'] == username]['user_id'].iloc[0])
        st.session_state['user'] = user_id

    # > if the authentication failed
    elif st.session_state['authentication_status'] == False:
        # write an error message on the sidebar
        with st.sidebar:
            st.error('Username/password is incorrect')

    # > if there are no authentication attempts yet (e.g., first time visitors)
    elif st.session_state['authentication_status'] == None:
        # write an warning message on the sidebar
        with st.sidebar:
            st.warning('Please enter your username and password in the sidebar')

    if 'user' not in st.session_state:
        st.session_state['user'] = 2