# agentome/ego_agent.py
from agentome.base import AgentBase

class EgoAgent(AgentBase):
    def run(self, parsed_data, strategy_outputs):
        preferred = next((s for s in strategy_outputs if "DP" in s["strategy"] or "Dynamic" in s["strategy"]), strategy_outputs[0])
        return {
            "problem": parsed_data['original'],
            "intro": parsed_data['problem_intro'],
            "examples": parsed_data['examples'],
            "categories": parsed_data['likely_categories'],
            "implementations": strategy_outputs,
            "best_solution": preferred
        }
