from resources import transcription
import streamlit as st
import json
import os
import boto3

# bedrock
session = boto3.Session()
bedrock_runtime = session.client('bedrock-runtime')


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


def perform_task(description, button_name):
    st.write(description)
    prompt_input = st.text_area("Prompt 입력", key=button_name)

    if st.button(button_name):
        prompt = f"<transcript>에는 상담원과 고객간의 통화 녹취가 기록되어 있습니다.\n<transcript>{transcription.transcription}</transcript>\n이 녹취를 읽고 답변해주세요.\n{prompt_input}"
        parameter = {
            "anthropic_version": "bedrock-2023-05-31",
            "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
            "max_tokens": 2048,
            "temperature": 0.3,
            "top_p": 0.999,
        }

        streaming_response = get_model_response(parameter, prompt)
        stream = streaming_response.get("body")
        with st.spinner("Claude is Thinking..."):
            st.write_stream(parse_stream(stream))

        with st.expander("Bedrock Parameter"):
            st.json({**parameter, "prompt": prompt})


# streamlit 앱
st.set_page_config(page_title="FSI Gen AI 데모")
st.title("옥탱크 보험 AI 고객 센터 [데모]")

# Info
st.subheader("자동차 보험 상담")
st.audio(os.path.join("resources", "transcription.mp3"))
with st.expander("녹취문 보기"):
    st.write(transcription.transcription)

# Tabs
summary, note, reply, quality = st.tabs(["요약", "상담노트", "메일 회신", "상담품질"])
with summary:
    perform_task("녹취된 상담의 상세한 요약을 생성합니다.", "요약 생성")
with note:
    perform_task("필요한 정보만 발췌할 수 있도록 요약 형식을 조정하세요.", "상담 노트 생성")
with reply:
    perform_task("고객에게 전달할 회신 메일을 생성하세요.", "회신 메일 생성")
with quality:
    perform_task("녹취에 대한 상세한 규정준수 및 품질을 검토합니다.", "상담 품질 검토 실행")
