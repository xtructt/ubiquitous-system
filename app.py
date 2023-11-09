import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
import time


    
class OpenAIAgent:
    
    def __init__(self):
        self.__client = OpenAI()
        self.__assistant = self.__client.beta.assistants.create(name="GPT-4", model="gpt-4-1106-preview")
        self.__thread = self.__client.beta.threads.create()
    
    def chat(self, message, history):
        chat_message = self.__client.beta.threads.messages.create(
            thread_id=self.__thread.id,
            role="user",
            content=message
        )
        user_chat_id = chat_message.id
        run = self.__client.beta.threads.runs.create(
            thread_id=self.__thread.id,
            assistant_id=self.__assistant.id,
        )
        status = run.status
        while status != "completed":   
            time.sleep(1)
            run = self.__client.beta.threads.runs.retrieve(
            thread_id=self.__thread.id,
            run_id=run.id
            )
            status = run.status
        list_message_filtered = self.__client.beta.threads.messages.list(
                                    thread_id=self.__thread.id,
                                    before=user_chat_id
                                    )
        for m in list_message_filtered.data:
            for m_content in m.content:
                yield m_content.text.value

if __name__ == "__main__":
    load_dotenv()  # take environment variables from .env.
    agent = OpenAIAgent()
    gr.ChatInterface(agent.chat).queue().launch()