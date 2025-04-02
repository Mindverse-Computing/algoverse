# agentome/memory_agent.py
from agentome.base import AgentBase

class MemoryAgent(AgentBase):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

    def run(self, parsed_data):
        return []  # Future: graph search

    def store(self, problem_data, strategies, implementations):
        self.graph.add_problem_with_context(problem_data, strategies, implementations)
