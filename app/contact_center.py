from resources import contact_center_transcription
import streamlit as st
import os
from modules.bedrock import get_model_streaming_response, MODEL_ID_INFO, parse_stream


# config
TASK_INFO = {
    # task_name: [description, button_name]
    "요약": ["녹취된 상담의 상세한 요약을 생성합니다.", "요약 생성"],
    "상담 노트": ["필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "상담 노트 생성"],
    "메일 회신": ["고객에게 전달할 회신 메일을 생성하세요.", "회신 메일 생성"],
    "상담 품질": ["녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "상담 품질 검토 실행"]
}
SYSTEM = f"<transcript>에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다. 이 녹취를 읽고 답변해주세요.\n\n<transcript>{contact_center_transcription.transcription}</transcript>\n"


def perform_task(task_name):
    description, button_name = TASK_INFO[task_name]

    if f'ta_{task_name}' not in st.session_state:
        st.session_state[f'ta_{task_name}'] = "Prompt를 입력하세요."
    # description
    st.write(description)

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()), key=f'mn_{task_name}')
    with st.expander("Claude Setting"):
        max_token = st.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048,
                                    key=f'mt_{task_name}', disabled=True)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, key=f't_{task_name}',
                                disabled=True)
        top_p = st.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f",
                                key=f'tp_{task_name}', disabled=True)
    prompt_input = st.text_area("User Prompt 입력", key=f'ta_{task_name}', height=400,
                                value=st.session_state[f'ta_{task_name}'])

    # button
    if st.button(button_name):
        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": MODEL_ID_INFO[model_name],
            "max_tokens": max_token,
            "temperature": temperature,
            "top_p": top_p,
        }
        prompt = f"<transcript>에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다.\n<transcript>{contact_center_transcription.transcription}</transcript>\n이 녹취를 읽고 답변해주세요.\n{prompt_input}"
        streaming_response = get_model_streaming_response(parameter, SYSTEM, prompt)

        # output
        stream = streaming_response.get("body")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))


def app():
    # app info
    st.subheader("자동차 보험 상담")
    st.audio(os.path.join("resources", "contact_center_transcription.mp3"))
    with st.expander("녹취문 보기"):
        st.write(contact_center_transcription.transcription)
    with st.expander("System Prompt"):
        st.write(SYSTEM)

    # task
    st.subheader("작업")
    summary, note, reply, quality = st.tabs(list(TASK_INFO.keys()))
    with summary:
        perform_task("요약")
    with note:
        perform_task("상담 노트")
    with reply:
        perform_task("메일 회신")
    with quality:
        perform_task("상담 품질")
