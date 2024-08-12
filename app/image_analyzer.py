import streamlit as st
import os
from modules.image import get_bytes_from_file
from modules.bedrock import MODEL_ID_INFO, get_model_image_response


# config
BASE_IMAGE_PATH = "visioning/images/"

PROMPT = """
Human: 당신은 이미지에서 정보를 파악하는 데이터 분석가입니다. 
이미지가 나타내는 내용을 파악하고 분석해 주세요.

<conditions>에 있는 내용들을 준수해주세요.
<steps>에 있는단계대로 수행해 주세요.

<conditions>
이미지 내에 수치가 있다면 구체적 수치도 포함해주세요.
그래프에는 기간이나 연도, 일자, 요일 등이 포함되어 있을 수도 있으니 주의하세요.
그래프의 경우 가로축과 수직축의 단위와 값을 올바르게 파악해주세요.
비교 데이터를 포함하는그래프의 경우 색깔을 잘 구분해서 파악해주세요.
이미지 자료 속의 항목이 색깔별로 표현되어 있을 수도 있으니 주의하세요.
이미지속 상단의 큰 글자의 경우, 이미지의 주제일 수 있습니다.
순위를 표현하고 있을 수 있으니 주의해주세요.
</condition>

<steps>
1.파악된 내용과 특징들을 출력해 주세요.
2.파악된 내용과 특징들 토대로 인포그래픽스의 보고서를 작성해주세요.
</steps>

Assistant:
"""


# 디스크의 파일에서 바이트 로드하기
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


# Streamlit 앱
def app():
    # app info
    st.subheader("Image Analyzer")

    # 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(BASE_IMAGE_PATH) if os.path.isfile(os.path.join(BASE_IMAGE_PATH, f))]
    selected_image = st.selectbox("이미지 선택", image_files)
    if selected_image:
        file_path = os.path.join(BASE_IMAGE_PATH, selected_image)
        st.image(file_path, caption=selected_image, width=600)

    # task
    st.subheader("작업")
    if 'session_image_analyzer' not in st.session_state:
        st.session_state['session_image_analyzer'] = "Prompt를 입력하세요."

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=4000, disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                disabled=True)

    prompt_input = st.text_area("User Prompt 입력", height=300, key="image_analyzer",
                                value=st.session_state['session_image_analyzer'])

    # button
    if st.button("이미지 분석"):
        # session 저장
        st.session_state['session_image_analyzer'] = prompt_input

        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }
        file_path = os.path.join(BASE_IMAGE_PATH, selected_image)
        image_bytes = get_bytes_from_file(file_path)
        image_type = "image/png" if selected_image.endswith(".png") else "image/jpeg"

        st.write("분석 결과:")
        with st.spinner("Analyzing..."):
            try:
                result = get_model_image_response(parameter, prompt_input, image_type, image_bytes)
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
