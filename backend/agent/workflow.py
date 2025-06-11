import os
import dspy
import mlflow

from datetime import datetime
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

lm = dspy.LM(
    model='openai/gpt-4o-mini',
    temperature=0,
    api_key=os.environ['OPENAI_API_KEY']
)

dspy.configure(lm=lm, async_max_workers=4)
mlflow.dspy.autolog(log_traces=True, log_evals=True, log_traces_from_eval=True, silent=True)
mlflow.set_experiment('deep-research-agent')


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


def web_search_tavily(query: str) -> str:
    """
    Search the web for current information, news, or public data. 
    Input should be a search query.
    """

    results = ''

    search_tool = TavilySearchResults(
        max_results=2,
        name='web_search'
    )

    for search_results in search_tool.invoke(query):
        search_result_str = ''
        search_result_str += f"Title: {search_results['title']}\n"
        search_result_str += f"Content: {search_results['content']}\n"
        results += search_result_str

    return results


class QueryWriterInstructions(dspy.Signature):
    f"""Your goal is to generate sophisticated and diverse web search queries. 
    These queries are intended for an advanced automated web research tool capable of analyzing complex results, following links, and synthesizing information.

    Instructions:
    - Always prefer a single search query, only add another query if the original question requests multiple aspects or elements and one query is not enough.
    - Each query should focus on one specific aspect of the original question.
    - Queries should be diverse, if the topic is broad, generate more than 1 query.
    - Don't generate multiple similar queries, 1 is enough.
    - Query should ensure that the most current information is gathered. The current date is {get_current_date()}.
    """

    research_topic: str =dspy.InputField(
        desc="The topic or question for which search queries are being generated."
    )
    num_queries: int = dspy.InputField(
        desc=f"The number of search queries to generate"
    )
    search_queries: list[str] = dspy.OutputField(
        desc="A list of search queries generated based on the research topic."
    )


class WebSearcherInstructions(dspy.Signature):
    f"""Conduct targeted web searches to gather the most recent, credible information on the input research topic and synthesize it into a verifiable text artifact.

    Instructions:
    - Query should ensure that the most current information is gathered. The current date is {get_current_date()}.
    - Conduct multiple, diverse searches to gather comprehensive information.
    - Consolidate key findings while meticulously tracking the source(s) for each specific piece of information.
    - The output should be a well-written summary or report based on your search findings.
    - Only include the information found in the search results, don't make up any information.
    """

    research_topic: str = dspy.InputField(
        desc="The topic or question for which search queries are being generated."
    )
    search_queries: list[str] = dspy.InputField(
        desc="A list of search queries generated based on the research topic."
    )
    findings: str = dspy.OutputField(
        desc="A well-written summary or report based on the search findings, including citations."
    )


class ReflectionInstructions(dspy.Signature):
    """You are an expert research assistant analyzing summaries.

    Instructions:
    - Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
    - If provided summaries are sufficient to answer the user's question, don't generate a follow-up query.
    - If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
    - Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.
    - Ensure the follow-up query is self-contained and includes necessary context for web search.
    - Reflect carefully on the summaries to identify knowledge gaps and produce a follow-up query.
    """

    research_topic: str = dspy.InputField(
        desc="The topic or question for which summaries are being analyzed."
    )
    summaries: list[str] = dspy.InputField(
        desc="A list of summaries to analyze for knowledge gaps."
    )
    is_sufficient: bool = dspy.OutputField(
        desc="Indicates whether the provided summaries are sufficient to answer the user's question."
    )
    knowledge_gap: str = dspy.OutputField(
        desc="Describes what information is missing or needs clarification."
    )
    follow_up_queries: list[str] = dspy.OutputField(
        desc="A list of specific questions to address the identified knowledge gap."
    )


class AnswerGeneratorInstructions(dspy.Signature):
    f"""Generate a high-quality answer to the user's question based on the provided summaries.

    Instructions:
    - The current date is {get_current_date()}.
    - You are the final step of a multi-step research process, don't mention that you are the final step.
    - You have access to all the information gathered from the previous steps.
    - You have access to the user's question.
    - Generate a high-quality answer to the user's question based on the provided summaries and the user's question.
    - You MUST include all the citations from the summaries in the answer correctly.
    """

    research_topic: str = dspy.InputField(
        desc="The topic or question for which the answer is being generated."
    )

    summaries: list[str] = dspy.InputField(
        desc="A list of summaries that provide information relevant to the user's question."
    )

    answer: str = dspy.OutputField(
        desc="A high-quality answer to the user's question, incorporating all relevant information from the summaries."
    )


class ReflectionWebAgent(dspy.Module):
    def __init__(self, max_iterations: int = 2, num_queries: int = 2):
        super().__init__()

        self.explore_more = True
        self.max_iterations = max_iterations
        self.num_queries = num_queries
        self.iteration_count = 0
        self.summaries = ''
        self.query_writer = dspy.ChainOfThought(QueryWriterInstructions)
        self.web_searcher = dspy.ReAct(WebSearcherInstructions, tools=[web_search_tavily])
        self.reflection = dspy.ChainOfThought(ReflectionInstructions)
        self.answer_generator = dspy.ChainOfThought(AnswerGeneratorInstructions)


    def forward(self, research_topic: str) -> str:
        """
        Main workflow for the research agent.
        Takes a research topic and returns a comprehensive answer.
        """

        # Step 1: Generate search queries
        query_writer_output = self.query_writer(research_topic=research_topic, num_queries=self.num_queries)
        search_queries = query_writer_output.search_queries

        while self.explore_more and self.iteration_count < self.max_iterations:
            print(f"Iteration {self.iteration_count + 1} for topic: {research_topic}")
            self.iteration_count += 1

            # Step 2: Conduct web searches
            search_output = self.web_searcher(
                research_topic=research_topic,
                search_queries=search_queries
            )

            self.summaries += search_output.findings

            # Step 3: Reflect on findings and identify knowledge gaps
            reflection = self.reflection(
                research_topic=research_topic,
                summaries=self.summaries
            )

            if reflection.is_sufficient:
                self.explore_more = False
            else:
                # If there are knowledge gaps, generate follow-up queries
                search_queries = reflection.follow_up_queries

        # Step 4: Generate final answer based on findings
        output = self.answer_generator(
            research_topic=research_topic,
            summaries=self.summaries
        )

        return output.answer
    
if __name__ == "__main__":
    agent = ReflectionWebAgent(max_iterations=5, num_queries=3)
    agent.save('backend/output/deep-research-agent', save_program=True)