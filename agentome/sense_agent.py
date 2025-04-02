# agentome/sense_agent.py
import json
from langchain.schema import HumanMessage
from agentome.base import AgentBase

class SenseAgent(AgentBase):
    def __init__(self, llm, memory=None):
        super().__init__(memory)
        self.llm = llm

    def run(self, problem_statement: str):
        prompt = (
            f"You are an expert coding interview tutor.\n"
            f"Given the following problem:\n{problem_statement}\n"
            f"Generate a JSON output with:\n"
            f"- problem_intro\n- examples (list of input/output)\n"
            f"- likely_categories\n- constraints"
        )
        response = self.llm([HumanMessage(content=prompt)]).content
        try:
            parsed = json.loads(response)
        except Exception:
            parsed = {
                "problem_intro": "This is a classic coding interview problem.",
                "examples": [],
                "likely_categories": [],
                "constraints": []
            }
        parsed["original"] = problem_statement
        parsed["keywords"] = problem_statement.lower().split()
        self.memory.save_context({"input": problem_statement}, {"sense_output": json.dumps(parsed)})
        return parsed
