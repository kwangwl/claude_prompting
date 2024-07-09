from resources import transcription
import streamlit as st
import json
import os
import boto3


# config
MODEL_ID_INFO = {
    "Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "Haiku": "anthropic.claude-3-haiku-20240307-v1:0"
}


# bedrock
if os.path.exists(".streamlit"):
    # local
    session = boto3.Session(
        aws_access_key_id=st.secrets["ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["SECRET_ACCESS_KEY"],
        region_name=st.secrets["REGION_NAME"],
    )
    bedrock_runtime = session.client('bedrock-runtime')
else:
    # claude9
    session = boto3.Session()
    bedrock_runtime = session.client('bedrock-runtime')


# function
def get_model_response(parameter, prompt):
    body = json.dumps({
        "anthropic_version": parameter["anthropic_version"],
        "max_tokens": parameter["max_tokens"],
        "temperature": parameter["temperature"],
        "top_p": parameter["top_p"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
    })

    streaming_response = bedrock_runtime.invoke_model_with_response_stream(body=body, modelId=parameter["model_id"])

    return streaming_response


def parse_stream(stream):
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            message = json.loads(chunk.get("bytes").decode())
            if message['type'] == "content_block_delta":
                yield message['delta']['text'] or ""
            elif message['type'] == "message_stop":
                return "\n"


def perform_task(parameter, description, button_name):
    st.write(description)
    prompt_input = st.text_area("Prompt 입력", key=button_name)

    if st.button(button_name):
        prompt = f"<transcript>에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다.\n<transcript>{transcription.transcription}</transcript>\n이 녹취를 읽고 답변해주세요.\n{prompt_input}"
        streaming_response = get_model_response(parameter, prompt)
        stream = streaming_response.get("body")
        with st.spinner("Processing..."):
            st.write_stream(parse_stream(stream))

        with st.expander("Bedrock Parameter"):
            st.json({**parameter, "prompt": prompt})


# streamlit 앱
st.set_page_config(page_title="FSI Gen AI 데모")
st.title("옥탱크 보험 AI 고객 센터 [데모]")
st.sidebar.selectbox("시나리오", ["FSI - 자동차 보험 상담"])

# bedrock setting
st.sidebar.subheader("Claude Setting")
model_name = st.sidebar.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))
max_token = st.sidebar.number_input(label="Max Token", min_value=0, step=1, max_value=4096, value=2048)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3)
top_p = st.sidebar.number_input(label="Top P", min_value=0.000, step=0.001, max_value=1.000, value=0.999, format="%f")

# Info
st.subheader("자동차 보험 상담")
st.audio(os.path.join("resources", "transcription.mp3"))
with st.expander("녹취문 보기"):
    st.write(transcription.transcription)

# Tabs
summary, note, reply, quality = st.tabs(["요약", "상담노트", "메일 회신", "상담품질"])
parameter = {
    "anthropic_version": "bedrock-2023-05-31",
    "model_id": MODEL_ID_INFO[model_name],
    "max_tokens": max_token,
    "temperature": temperature,
    "top_p": top_p,
}

with summary:
    perform_task(parameter, "녹취된 상담의 상세한 요약을 생성합니다.", "요약 생성")
with note:
    perform_task(parameter, "필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "상담 노트 생성")
with reply:
    perform_task(parameter, "고객에게 전달할 회신 메일을 생성하세요.", "회신 메일 생성")
with quality:
    perform_task(parameter, "녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "상담 품질 검토 실행")
