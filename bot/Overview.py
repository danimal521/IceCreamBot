import streamlit as st  
from style import global_page_style2
import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_ACCOUNT: str                                               = os.environ["openai_account"]  #URL of the Azure OpenAI resource
AZURE_DEPLOYMENT_MODEL: str                                             = os.environ["model"] #Deployment model name
AZURE_OPENAI_KEY: str                                                   = os.environ["openai_key"] #API key for Azure OpenAI
service_endpoint                                                        = os.environ["search_service"] #URL of the Azure Search service
index_name                                                              = os.environ["index"] #Name of the Azure Search index
key                                                                     = os.environ["search_key"] #API key for Azure Search

search_client                                                           = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))



def chat(messages, question):  
    
    with st.chat_message("user", avatar="👤"):  
        st.markdown(question)  
    with st.spinner('Processing...'): 
        messages.append({"role": "assistant", "content": "🤖: " + question})  

        GROUNDED_PROMPT="""
        You are a friendly assistant that answers questions about ice cream.
        answer the question with only the information provided in the sources.
        If there isn't enough information below, say you don't know.
        Do not generate answers that don't use the sources below.      
        Sources:\n{sources}   
        """

        search_results = search_client.search(
            search_text=question,
            top=5,
            select="chunk"
        )
        sources_formatted = "\n".join([f'{document["chunk"]}' for document in search_results])

        client = AzureOpenAI(
            api_key=AZURE_OPENAI_KEY,  
            api_version="2024-07-01-preview",
            azure_endpoint=AZURE_OPENAI_ACCOUNT)

        print(GROUNDED_PROMPT.format(sources=sources_formatted))

        #st.text(GROUNDED_PROMPT.format(sources=sources_formatted))

        chat_completion = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_MODEL,
        
        messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": GROUNDED_PROMPT.format(sources=sources_formatted)
                }
            ]
        },
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=0.7,
    top_p=0.5
    )

    print(chat_completion.choices[0].message.content)

    messages.append({"role": "assistant", "content": "🤖: " + question})  
    with st.chat_message("assistant", avatar="🤖"):  
        st.markdown(chat_completion.choices[0].message.content)  
  
def clear_session(messages):  
    # Clear necessary session state variables  
    st.cache_data.clear()  
    messages.clear()  
    return messages  
  
def main():  
    dirname = os.path.dirname(os.path.abspath(__file__))
    st.logo(dirname + '/pages/logo-gray.png', size="large")

    st.title("Ice Cream Bot")  
    st.write("-"*50)

    if 'messages' not in st.session_state:  
        st.session_state.messages = []  
  
    for message in st.session_state.messages:  
        with st.chat_message(message["role"], avatar="✔️"):  
            st.markdown(message['content'])  
   
    question = st.chat_input('Ask your ice cream question here... ')  
    if question:  
        chat(st.session_state.messages, question)  
        st.write('-'*50)
    clear_chat_placeholder = st.empty()  
    if clear_chat_placeholder.button('Start New Session'):  
        st.session_state.messages = clear_session(st.session_state.messages)  
        clear_chat_placeholder.empty()  
        st.success("Ice Cream Bot session has been reset.")  
  
if __name__ == '__main__':  
    global_page_style2()  
    main()  
