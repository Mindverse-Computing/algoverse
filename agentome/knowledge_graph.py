# agentome/knowledge_graph.py
import json
from uuid import uuid4
from neo4j import GraphDatabase

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_problem_with_context(self, problem_data, strategies, implementations):
        with self.driver.session() as session:
            pid = str(uuid4())
            session.run(
                """
                MERGE (p:Problem {id: $pid})
                SET p.title = $title,
                    p.description = $desc,
                    p.difficulty = 'Unknown',
                    p.tags = $tags,
                    p.examples = $examples
                """,
                pid=pid,
                title=problem_data['original'],
                desc=problem_data['problem_intro'],
                tags=problem_data.get('likely_categories', []),
                examples=[json.dumps(ex) for ex in problem_data.get('examples', [])]
            )

            for name, desc in strategies.items():
                session.run(
                    """
                    MERGE (s:Strategy {name: $name})
                    SET s.description = $desc
                    WITH s
                    MATCH (p:Problem {id: $pid})
                    MERGE (p)-[:USES_STRATEGY]->(s)
                    """,
                    name=name, desc=desc, pid=pid
                )

            for impl in implementations:
                cid = str(uuid4())
                session.run(
                    """
                    CREATE (c:CodeSnippet {
                        id: $cid,
                        language: 'Python',
                        code: $code,
                        complexity: 'Unknown',
                        walkthrough: $desc
                    })
                    WITH c
                    MATCH (s:Strategy {name: $strategy})
                    MERGE (s)-[:IMPLEMENTED_BY]->(c)
                    """,
                    cid=cid,
                    code=impl['code'],
                    desc=impl['description'],
                    strategy=impl['strategy']
                )
