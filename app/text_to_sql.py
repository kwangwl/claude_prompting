import streamlit as st
from modules.bedrock import get_model_response, MODEL_ID_INFO
from modules.database import query_sqlite
from resources.text_to_sql_db_context import context
import os


def app():
    # app info
    st.subheader("데이터베이스 (SQLite)")
    with st.expander("데이터베이스 보기"):
        st.image(os.path.join("resources", "text_to_sql_db.png"))

    # task
    st.subheader("작업")

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048, disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                disabled=True)
    prompt_input = st.text_area("Prompt 입력")

    # action
    st.subheader("자연어 쿼리 입력")
    with st.expander("Query 예시"):
        st.text("주문 ID가 1인 주문 항목의 제품 이름과 수량\n가격이 20보다 큰 모든 제품\n2023년 1월 1일 이후에 작성된 모든 리뷰")
    user_query = st.text_input("Query:")

    # button
    if st.button("SQL 생성 및 데이터 쿼리"):
        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }

        prompt = f"{context}\n\n{prompt_input}Human:{user_query}"
        generated_sql = get_model_response(parameter, prompt)

        st.write("생성된 SQL:")
        st.code(generated_sql, language='sql')

        try:
            result = query_sqlite(generated_sql)
            st.write("쿼리 결과:")
            st.dataframe(result)

        except Exception as e:
            st.write("에러 발생:")
            st.error(str(e))

        with st.expander("Bedrock Parameter"):
            st.json({**parameter, "prompt": prompt})
