import streamlit as st
import os
from modules.image import get_bytes_from_file
from modules.bedrock import MODEL_ID_INFO, get_model_image_response, parse_stream


# config
BASE_IMAGE_PATH = "resources/vision/"
IMAGE_FILES = [f for f in os.listdir(BASE_IMAGE_PATH) if os.path.isfile(os.path.join(BASE_IMAGE_PATH, f))]


# Streamlit 앱
def app():
    # app info
    st.subheader("Vision Analyzer")

    # 이미지 파일 목록 가져오기
    selected_image = st.selectbox("이미지 선택", IMAGE_FILES)
    if selected_image:
        file_path = os.path.join(BASE_IMAGE_PATH, selected_image)
        st.image(file_path, caption=selected_image, width=500)

    if 'session_vision_analyzer' not in st.session_state:
        st.session_state['session_vision_analyzer'] = "Prompt를 입력하세요."

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))

    prompt_input = st.text_area("User Prompt 입력", height=300, key="vision_analyzer",
                                value=st.session_state['session_vision_analyzer'])

    # 폼 제출 버튼
    submit_button = st.button("이미지 분석")

    # button
    if submit_button:
        # session 저장
        st.session_state['session_vision_analyzer'] = prompt_input

        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": 2048,
            "temperature": 0.0,
            'top_p': 0.999
        }
        file_path = os.path.join(BASE_IMAGE_PATH, selected_image)
        image_bytes = get_bytes_from_file(file_path)
        image_type = "image/png" if selected_image.endswith(".png") else "image/jpeg"

        streaming_response = get_model_image_response(parameter, prompt_input, image_type, image_bytes)

        # output
        stream = streaming_response.get("body")
        st.write("비전 분석 결과:")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))
