import streamlit as st
from modules.bedrock import get_model_streaming_response, MODEL_ID_INFO, parse_stream
from resources.text_to_sql_db import schema
import os


# config
SYSTEM = f"아래 <scheme>에는 테이블 스키마 정보를 포함하고 있습니다. 이 스키마 정보를 기반으로 쿼리를 작성해주세요.\n\n<scheme>\n{schema}</scheme>\n"


def app():
    # app info
    st.subheader("데이터베이스 (SQLite)")
    with st.expander("데이터베이스 보기"):
        st.image(os.path.join("resources", "text_to_sql_db.png"))
    with st.expander("System Prompt"):
        st.write(SYSTEM)

    # task
    if 'session_text2sql' not in st.session_state:
        st.session_state['session_text2sql'] = "Prompt를 입력하세요."

    st.subheader("작업")

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048, disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                disabled=True)

    prompt_input = st.text_area("User Prompt 입력", height=300, key="text-to-sql",
                                value=st.session_state['session_text2sql'])

    # button
    if st.button("쿼리 생성"):
        # session 저장
        st.session_state['session_text2sql'] = prompt_input

        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }
        prompt = f"{SYSTEM}\n\n{prompt_input}"
        streaming_response = get_model_streaming_response(parameter, prompt)

        # output
        stream = streaming_response.get("body")
        st.write("생성된 SQL:")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))
