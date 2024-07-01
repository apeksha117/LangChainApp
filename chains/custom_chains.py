from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate


from output_parsers import summary_parser, ice_breaker_parser, topics_of_interest_parser

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_creative = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")


def get_summary_chain() -> RunnableSequence:
    summary_template = """ given the Linkedin information {linkedin_data} and twitter data {twitter_data} about a person I want you to create: 
    1. Name of the person 
    2. Location from twitter account 
    3. A short summary 
    4. two interesting facts about them 
    5. Number of twitter followers 
    6. number of tweets 
    Use both linked data as well as twitter data to generate your response \n{format_instructions} """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_data", "twitter_data"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    return summary_prompt_template | llm | summary_parser


def get_interests_chain() -> RunnableSequence:
    interesting_facts_template = """
         given the information about a person from linkedin {linkedin_data}, and twitter posts {twitter_data} I want you to create:
         3 topics that might interest them
        \n{format_instructions}
     """

    interesting_facts_prompt_template = PromptTemplate(
        input_variables=["linkedin_data", "twitter_data"],
        template=interesting_facts_template,
        partial_variables={
            "format_instructions": topics_of_interest_parser.get_format_instructions()
        },
    )

    return interesting_facts_prompt_template | llm | topics_of_interest_parser


def get_ice_breaker_chain() -> RunnableSequence:
    ice_breaker_template = """
         given the information about a person from linkedin {linkedin_data}, and twitter posts {twitter_data} I want you to create:
         2 creative Ice breakers with them that are derived from their activity on Linkedin and twitter, preferably on latest tweets
        \n{format_instructions}
     """

    ice_breaker_prompt_template = PromptTemplate(
        input_variables=["linkedin_data", "twitter_data"],
        template=ice_breaker_template,
        partial_variables={
            "format_instructions": ice_breaker_parser.get_format_instructions()
        },
    )

    return ice_breaker_prompt_template | llm | ice_breaker_parser
