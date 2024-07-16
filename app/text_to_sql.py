import streamlit as st
from modules.bedrock import get_model_streaming_response, MODEL_ID_INFO, parse_stream
from resources.text_to_sql_system import system
import os


def app():
    # app info
    st.subheader("데이터베이스 (SQLite)")
    with st.expander("데이터베이스 보기"):
        st.image(os.path.join("resources", "text_to_sql_db.png"))
    with st.expander("System Prompt"):
        st.write(system)

    # task
    st.subheader("작업")

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048, disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                disabled=True)

    prompt_input = st.text_area("User Prompt 입력", height=300)

    # button
    if st.button("쿼리 생성"):
        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }
        streaming_response = get_model_streaming_response(parameter, system, prompt_input)

        # output
        stream = streaming_response.get("body")
        st.write("생성된 SQL:")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))
