import boto3
import json
import base64
import logging
import os
from io import BytesIO

logging.basicConfig(format="%(asctime)s %(name)s [%(levelname)s] %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_IMAGE_PATH = "images/"
BASE_REPORT_PATH = "reports/"


# 파일 바이트에서 BytesIO 객체 가져오기
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


# 파일 바이트에서 base64로 인코딩된 문자열 가져오기
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


# 디스크의 파일에서 바이트 로드하기
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


# InvokeModel API 호출에 대한 문자열화된 요청 본문 가져오기
def get_image_understanding_request_body(prompt, image_bytes=None, image_type="image/jpeg", mask_prompt=None,
                                         negative_prompt=None):
    input_image_base64 = get_base64_from_bytes(image_bytes)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0,
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
    }

    return json.dumps(body)


def get_image_list():
    file_list = []
    index = 0
    for entry in os.listdir(BASE_IMAGE_PATH):
        if os.path.isfile(os.path.join(BASE_IMAGE_PATH, entry)):
            logger.info(f"{index} : {entry}")
            index = index + 1
            file_list.append(entry)

    return file_list


# Anthropic Claude를 사용하여 응답 생성하기
def get_response_from_model(prompt_content, image_bytes, image_type, mask_prompt=None):
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-west-2",
    )

    body = get_image_understanding_request_body(prompt_content, image_bytes, image_type, mask_prompt=mask_prompt)

    response = bedrock.invoke_model(
        body=body,
        # modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response.get('body').read())

    output = response_body['content'][0]['text']
    logger.info(output)

    return output


def get_content_type_by_extension(ext):
    return "image/png" if ext == ".png" else "image/jpeg"


def get_file_name_ext(file_name):
    return os.path.splitext(file_name)[1]


def get_result_single(file_name):
    file_path = os.path.join(BASE_IMAGE_PATH, file_name)
    image_bytes = get_bytes_from_file(file_path)
    image_type = get_content_type_by_extension(get_file_name_ext(file_name))

    logger.info("image file : " + file_name)

    try:
        result = get_response_from_model(
            prompt_content=prompt_text,
            image_bytes=image_bytes,
            image_type=image_type
        )

        write_report(file_name, result)
    except:
        logger.info("Error")


def write_report(file_name, content):
    report_file_name = os.path.splitext(file_name)[0]
    report_file = open(f"{BASE_REPORT_PATH}{report_file_name}.txt", "a")
    report_file.write(content)
    report_file.write("\n------------------------------\n\n")
    report_file.close()


def get_result_all(image_list):
    for image_file in image_list:
        get_result_single(image_file)


prompt_text = """ 

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

import sys

if __name__ == '__main__':
    args = sys.argv

    image_list = get_image_list()

    if args[1] == "A":
        get_result_all(image_list)
    else:
        get_result_single(image_list[int(args[1])])

