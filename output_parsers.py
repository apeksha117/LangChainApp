from typing import List, Dict, Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Summary(BaseModel):
    name_of_person: str = Field(description="Name of the person")
    location: str = Field(description="Location from twitter account ")
    twitter_follower: str = Field(description="Number of twitter followers")
    summary: str = Field(description="summary")
    number_of_tweets: str = Field(description="number of tweets")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
            "name_of_person": self.name_of_person,
            "location": self.location,
            "twitter_follower": self.twitter_follower,
            "number_of_tweets": self.number_of_tweets,
        }


class IceBreaker(BaseModel):
    ice_breakers: List[str] = Field(description="ice breaker list")

    def to_dict(self) -> Dict[str, Any]:
        return {"ice_breakers": self.ice_breakers}


class TopicOfInterest(BaseModel):
    topics_of_interest: List[str] = Field(
        description="topic that might interest the person"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {"topics_of_interest": self.topics_of_interest}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
ice_breaker_parser = PydanticOutputParser(pydantic_object=IceBreaker)
topics_of_interest_parser = PydanticOutputParser(pydantic_object=TopicOfInterest)
