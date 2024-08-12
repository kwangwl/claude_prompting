from modules.session import get_client
from modules.image import get_base64_from_bytes
import json


MODEL_ID_INFO = {
    "Sonnet 3.5": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "Haiku": "anthropic.claude-3-haiku-20240307-v1:0"
}


def get_model_response(parameter, system, prompt):
    bedrock_runtime = get_client('bedrock-runtime')

    body = json.dumps({
        "anthropic_version": parameter["anthropic_version"],
        "max_tokens": parameter["max_tokens"],
        "temperature": parameter["temperature"],
        "top_p": parameter["top_p"],
        "system": system,
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

    response = bedrock_runtime.invoke_model(body=body, modelId=parameter["model_id"])
    response_body = json.loads(response.get('body').read())  # response 읽기
    result = response_body.get("content")[0].get("text")

    return result


def get_model_streaming_response(parameter, prompt):
    bedrock_runtime = get_client('bedrock-runtime')

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


def get_model_image_response(parameter, prompt, image_type, image_bytes):
    bedrock_runtime = get_client('bedrock-runtime')
    input_image_base64 = get_base64_from_bytes(image_bytes)

    body = json.dumps({
        "anthropic_version": parameter["anthropic_version"],
        "max_tokens": parameter["max_tokens"],
        "temperature": parameter["temperature"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_type,
                            "data": input_image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
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
