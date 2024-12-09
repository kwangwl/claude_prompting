import streamlit as st
from modules.bedrock import retrieve_and_generate, MODEL_ID_INFO


# Config
KNOWLEDGE_BASE_ID = ""


def app():
    st.subheader('RAG Using Knowledge Base from Amazon Bedrock')

    # bedrock parameter
    model_name = st.selectbox("Select Model (Claude 3)", list(MODEL_ID_INFO.keys()))

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input('Enter your question here...')
    if question:
        st.session_state.chat_history.append({"role": 'user', "text": question})
        st.session_state.chat_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner('Thinking...'):
            parameter = {"kb_id": KNOWLEDGE_BASE_ID, "model_id": MODEL_ID_INFO[model_name]}
            response = retrieve_and_generate(question, parameter)

        if 'output' in response:
            answer = response['output']['text']
            st.session_state.chat_history.append({"role": 'assistant', "text": answer})
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

            if len(response['citations'][0]['retrievedReferences']) != 0:
                with st.expander("📚 View Context and Sources"):
                    for i, reference in enumerate(response['citations'][0]['retrievedReferences'], 1):
                        context = reference['content']['text']
                        doc_url = reference['location']['s3Location']['uri']

                        st.markdown(f"**Reference {i}:**")
                        st.markdown(context)
                        st.markdown(f"<span style='color:#FFDA33'>Source Document:</span> {doc_url}",
                                    unsafe_allow_html=True)
                        st.markdown("---")
            else:
                st.info("No additional context available for this response.")
        else:
            st.error("Failed to get a response. Please try again.")

    st.markdown("---")
