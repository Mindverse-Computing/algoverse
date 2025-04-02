# agentome/system.py
import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from agentome.sense_agent import SenseAgent
from agentome.memory_agent import MemoryAgent
from agentome.intellect_agent import IntellectAgent
from agentome.action_agent import StrategyActionAgent
from agentome.ego_agent import EgoAgent
from agentome.knowledge_graph import KnowledgeGraph

class MultiAgentSystem:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.graph = KnowledgeGraph(
            os.getenv("NEO4J_URI"),
            os.getenv("NEO4J_USER"),
            os.getenv("NEO4J_PASSWORD")
        )
        self.sense = SenseAgent(self.llm, self.memory)
        self.memory_agent = MemoryAgent(self.graph)
        self.intellect = IntellectAgent(self.llm, self.memory)
        self.ego = EgoAgent(self.memory)

    def solve_problem(self, problem_statement):
        parsed = self.sense.run(problem_statement)
        memory_examples = self.memory_agent.run(parsed)
        strategies = self.intellect.run(parsed, memory_examples)

        implementations = []
        for name, desc in strategies.items():
            action = StrategyActionAgent(name, desc, self.llm, self.memory)
            implementations.append(action.run(parsed))

        summary = self.ego.run(parsed, implementations)
        self.memory_agent.store(parsed, strategies, implementations)
        return summary
