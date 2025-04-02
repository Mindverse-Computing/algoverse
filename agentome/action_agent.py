# agentome/action_agent.py
from langchain.schema import HumanMessage
from agentome.base import AgentBase

class StrategyActionAgent(AgentBase):
    def __init__(self, strategy_name, strategy_desc, llm, memory=None):
        super().__init__(memory)
        self.strategy_name = strategy_name
        self.strategy_desc = strategy_desc
        self.llm = llm

    def run(self, parsed_data):
        prompt = (
            f"You are a Python engineer. Given the problem:\n"
            f"{parsed_data['original']}\n\n"
            f"Write a Python solution using the '{self.strategy_name}' strategy. "
            f"Add comments, time/space complexity, and a walkthrough.\n"
        )
        code = self.llm([HumanMessage(content=prompt)]).content.strip()
        return {
            "strategy": self.strategy_name,
            "description": self.strategy_desc,
            "code": code
        }
