import streamlit as st
import boto3
import os


if os.path.exists(".streamlit"):
    # local
    session = boto3.Session(
        aws_access_key_id=st.secrets["ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["SECRET_ACCESS_KEY"],
        region_name=st.secrets["REGION_NAME"],
    )
else:
    # claude9
    session = boto3.Session()


def get_client(client_name):
    return session.client(client_name)
