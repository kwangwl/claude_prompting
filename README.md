FSI Prompt 데모

실습 환경조건
1. AWS Cloud9 (us-west-2 리전, bedrock claude3 지원 리전)
2. bedrock model access - claude3 sonnet

실습 환경설정
1. AWS Cloud9 IDE에서 bash terminal을 선택합니다.
2. 터미널에 다음을 붙여넣고 실행하여 git 코드를 다운로드 받습니다.
- git clone https://github.com/kwangwl/fsi_prompt_demo.git
3. 다음 명령어를 입력하여 폴더를 이동합니다.
- cd fsi_prompt_demo
4. 다음 명령어를 입력하여 실습에 필요한 종속성을 설치합니다.
- pip install -r requirements.txt
5. 다음 명령어를 입력하여 application 을 실행합니다.
- streamlit run home.py --server.port 8080
6. AWS Cloud9에서 Preview -> Preview Running Application을 선택합니다.
7.어플리케이션이 실행된 웹페이지가 표시됩니다.

Ref
1. https://fsi-demo.mobilebigbang.com/
