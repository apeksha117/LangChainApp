from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties import linkedin
from third_parties import twitter
from dotenv import load_dotenv
import os
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import get_user_details
from output_parsers import Summary, summary_parser
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def ice_break_with(
    name: str,
) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    twitter_data = get_user_details(username=twitter_username)

    summary_template = """ given the Linkedin information {linkedin_data} and twsitter data {twitter_data} about a person I want you to create: 
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
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")  # type: ignore
    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(
        input={"linkedin_data": linkedin_data, "twitter_data": twitter_data}
    )

    return (
        res,
        linkedin_data.get("profile_pic_url"),
    )


if __name__ == "__main__":
    print("Strat Application")
    ice_break_with(name="Apeksha Agrawal")
    # pass
