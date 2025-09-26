import streamlit as st
from supabase import create_client
import uuid

# change only here

TITLE = "Treasure Hunt"
TABLE = "treasure"
mbno = "7219874336"
BUCKET = "QR"

st.set_page_config(page_title=TITLE,page_icon="💰")

st.title(TITLE)

supabase = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])

if "fees" not in st.session_state:
    st.session_state.fees = None

with st.expander("User Data",expanded=True):

    col1,col2 = st.columns(2)
    with col1:

        name = st.text_input("**Enter Name:**")
        gmail = st.text_input("**Enter Email:**")
        if gmail and not gmail.endswith("@gmail.com"):
            st.error("Enter Valid Gmail")

    with col2:

        branch = st.radio("Enter Branch:",["CSE","AIDS","MECH","CIVIL","E&TC"])
        phno = st.text_input("**Enter Phone Number:**",max_chars=10)
        if phno and (not phno.isdigit() or len(phno) != 10):
            st.error("Enter a valid 10-digit phone number")

    
    col1 , col2 = st.columns(2)
    if branch not in ["CSE", "AIDS"]:
        with col1:
            st.image("treasure.jpg")
            file = st.file_uploader("Upload screenshot of payment")
            if file:
                nam = f"QR-{uuid.uuid4()}-{file.name}"
                supabase.storage.from_(BUCKET).upload(nam, file.read(), {"content-type": file.type})
                st.session_state.fees = "online"

        with col2:
            st.write("Contact to us")
            st.write(mbno)
            obutt = st.button("Select")
            if obutt:
                st.session_state.fees = "offline"
    
    col1,col2,col3 = st.columns([1,1,1])
    with col2:
        butt = st.button("Submit")
    
    if butt :
        if name and gmail and branch and phno and (branch  in ["CSE", "AIDS"] or st.session_state.fees):
            res = supabase.table(TABLE).select("*").eq("email", gmail).execute().data     
            if res :
                st.success("You Already Enrolled")
            else:
                
                st.success(" Enrolled Successfully")
                supabase.table(TABLE).insert({
                        "name": name, "email": gmail, "branch":branch, "phone":phno , "fee":st.session_state.fees
                    }).execute()
                st.balloons()
                
        else:
            st.error("Fill all Fileds")
