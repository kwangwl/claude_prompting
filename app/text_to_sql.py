import streamlit as st
from modules.bedrock import get_model_response, MODEL_ID_INFO
from modules.database import query_sqlite
from resources.text_to_sql_db_context import context
import os


# SQL 생성 함수 (여기서는 간단한 예시로 더미 함수 사용)
def generate_sql_from_text(parameter, prompt_input, user_query):
    # 실제로는 자연어를 SQL로 변환하는 로직 필요
    final_prompt = f"{context}\n\n{prompt_input}Human:{user_query}"
    return get_model_response(parameter, final_prompt)


def app():
    st.subheader("데이터베이스 (SQLite)")
    with st.expander("Database 관계도"):
        st.image(os.path.join("resources", "text_to_sql_db.png"))

    with st.expander("Query 예시"):
        st.text("모든 직원의 이름과 급여\n모든 프로젝트의 이름과 시작일\nJohn Doe가 속한 프로젝트와 그의 역할")

    st.subheader("작업")
    # bedrock setting
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048, disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                disabled=True)
    prompt_input = st.text_area("Prompt 입력")

    st.subheader("자연어 쿼리 입력")
    user_query = st.text_input("쿼리:")
    if st.button("SQL 생성 및 데이터 쿼리"):
        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }
        generated_sql = generate_sql_from_text(parameter, prompt_input, user_query)

        st.write("생성된 SQL:")
        st.code(generated_sql, language='sql')

        try:
            result = query_sqlite(generated_sql)
            st.write("쿼리 결과:")
            st.dataframe(result)
        except Exception as e:
            st.write("에러 발생:")
            st.error(str(e))
            # 오류 수정 로직 추가 가능
            corrected_sql = generated_sql.replace("employees", "corrected_employees")
            st.write("수정된 SQL:")
            st.code(corrected_sql, language='sql')
            result = query_sqlite(corrected_sql)
            st.write("수정된 쿼리 결과:")
            st.dataframe(result)
