from backend.agent.workflow import ReflectionWebAgent

agent = ReflectionWebAgent(max_iterations=2, num_queries=2)

test_query = "Is Starlink available in India?"
result = agent(test_query)
print(f"Final answer for '{test_query}': {result}")