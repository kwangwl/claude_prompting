from resources import contact_center_transcription
import streamlit as st
import os
from modules.bedrock import get_model_streaming_response, MODEL_ID_INFO, parse_stream


# config
TASK_INFO = {
    # scenario_name: [key_name, description, button_name]
    "1. 요약": ["summary", "녹취된 상담의 상세한 요약을 생성합니다.", "요약 생성"],
    "2. 상담 노트": ["note", "필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "상담 노트 생성"],
    "3. 메일 회신": ["reply", "고객에게 전달할 회신 메일을 생성하세요.", "회신 메일 생성"],
    "4. 상담 품질": ["quality", "녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "상담 품질 검토 실행"]
}
SYSTEM = f"<transcript>에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다. 이 녹취를 읽고 답변해주세요.\n\n<transcript>{contact_center_transcription.transcription}</transcript>\n"


def perform_task(task_name):
    key_name, description, button_name = TASK_INFO[task_name]

    # session 초기화
    if f'session_{key_name}' not in st.session_state:
        st.session_state[f'session_{key_name}'] = "Prompt를 입력하세요."

    # description
    st.write(description)
    st.write("\n")

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()), key=f'model_name_{key_name}')
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048,
                                    key=f'max_token_{key_name}', disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, key=f'temperature_{key_name}',
                                disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                key=f'top_p_{key_name}', disabled=True)
    prompt_input = st.text_area("User Prompt 입력", key=f'prompt_input_{key_name}', height=400,
                                value=st.session_state[f'session_{key_name}'])

    # button
    if st.button(button_name):
        # session 저장
        st.session_state[f'session_{key_name}'] = prompt_input

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
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))


def app():
    # app info
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("자동차 보험 상담")
    with col2:
        st.link_button("FSI 데모 링크", "https://fsi-demo.mobilebigbang.com/")
    st.audio(os.path.join("resources", "contact_center_transcription.mp3"))
    with st.expander("녹취문 보기"):
        st.write(contact_center_transcription.transcription)
    with st.expander("System Prompt"):
        st.write(SYSTEM)

    # task
    st.subheader("작업")
    scenario_name = st.selectbox("시나리오 선택", list(TASK_INFO.keys()))
    perform_task(scenario_name)
    """
    summary, note, reply, quality = st.tabs(list(TASK_INFO.keys()))
    with summary:
        perform_task("요약")
    with note:
        perform_task("상담 노트")
    with reply:
        perform_task("메일 회신")
    with quality:
        perform_task("상담 품질")
    """
