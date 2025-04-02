# agentome/intellect_agent.py
import json
from langchain.schema import HumanMessage
from agentome.base import AgentBase

class IntellectAgent(AgentBase):
    def __init__(self, llm, memory=None):
        super().__init__(memory)
        self.llm = llm

    def run(self, parsed_data, memory_examples):
        prompt = (
            f"You are an algorithm strategist. Given the problem and examples, suggest 2-3 strategies as JSON.\n"
            f"Problem: {parsed_data['original']}\n"
            f"Examples: {json.dumps(parsed_data.get('examples', []))}\n"
            f"Respond as {{'StrategyName': 'Short description'}}."
        )
        response = self.llm([HumanMessage(content=prompt)]).content
        try:
            return json.loads(response)
        except Exception:
            return {
                "Brute Force": "Try all pairs.",
                "Hash Map": "Use dictionary to store complements."
            }
