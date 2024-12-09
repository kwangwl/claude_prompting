import streamlit as st
from modules.bedrock import get_model_streaming_response, MODEL_ID_INFO, parse_stream
from resources.text_to_sql.text_to_sql_db import schema
import os


# config
SYSTEM = f"""
아래 <scheme>에는 테이블 스키마 정보를 포함하고 있습니다. 이 스키마 정보를 기반으로 쿼리를 작성해주세요.

<scheme>
{schema}
</scheme>
"""


def app():
    # app info
    st.subheader("데이터베이스 (SQLite)")
    with st.expander("데이터베이스 보기"):
        st.image(os.path.join("resources", "text_to_sql", "text_to_sql_db.png"))
    with st.expander("System Prompt"):
        st.write(SYSTEM)

    st.subheader("작업")

    if 'session_text2sql' not in st.session_state:
        st.session_state['session_text2sql'] = "Prompt를 입력하세요."

    st.subheader("작업")
    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    prompt_input = st.text_area("User Prompt 입력", height=300, key="text-to-sql",
                                value=st.session_state['session_text2sql'])

    # 폼 제출 버튼
    submit_button = st.button("쿼리 생성")

    # button
    if submit_button:
        # session 저장
        st.session_state['session_text2sql'] = prompt_input

        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": 2048,
            "temperature": 0.0,
            'top_p': 0.999
        }
        prompt = f"{SYSTEM}\n\n{prompt_input}"
        streaming_response = get_model_streaming_response(parameter, prompt)

        # output
        stream = streaming_response.get("body")
        st.write("생성된 SQL:")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))
