# agentome/base.py
from langchain.memory import ConversationBufferMemory

class AgentBase:
    def __init__(self, memory: ConversationBufferMemory = None):
        self.memory = memory or ConversationBufferMemory(memory_key="chat_history")
