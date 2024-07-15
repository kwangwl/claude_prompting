from common.session import get_client
import json


MODEL_ID_INFO = {
    "Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "Haiku": "anthropic.claude-3-haiku-20240307-v1:0"
}


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


def parse_stream(stream):
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            message = json.loads(chunk.get("bytes").decode())
            if message['type'] == "content_block_delta":
                yield message['delta']['text'] or ""
            elif message['type'] == "message_stop":
                return "\n"
