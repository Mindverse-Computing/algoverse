# examples/solve_problem.py

import os
from dotenv import load_dotenv
from agentome.system import MultiAgentSystem

load_dotenv()

def main():
    print("\n🔍 Welcome to Codebrain: The Thinking Engine for Coding Problems\n")
    problem = input("Enter a Python coding interview problem:\n> ")

    print("\n🤖 Solving with multi-agent reasoning...\n")
    agentome = MultiAgentSystem()
    result = agentome.solve_problem(problem)

    print("\n🧠 Problem Introduction:")
    print(result['intro'])

    print("\n📘 Examples:")
    for ex in result['examples']:
        print(f"- Input: {ex.get('input', '-')}, Output: {ex.get('output', '-')}")

    print("\n🔎 Categories:", ", ".join(result['categories']) or "N/A")

    print("\n🧩 Implemented Strategies:")
    for impl in result['implementations']:
        print(f"\n--- Strategy: {impl['strategy']} ---")
        print("Description:", impl['description'])
        print("Code:\n", impl['code'])

    print("\n✅ Best Strategy Selected:")
    print(result['best_solution']['code'])

if __name__ == "__main__":
    main()
