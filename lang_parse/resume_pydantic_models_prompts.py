from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

class BasicInfo(BaseModel):
    name: str = Field(description="name of the candidate")
    bio: str = Field(description="summary or profile of the candidate")
    job_title: str = Field(description="current or latest job title")
    location: Optional[str]
    phone: Optional[str]

basic_info_parser = PydanticOutputParser(pydantic_object=BasicInfo)

basic_details_prompt = PromptTemplate(
    template="""
Extract the candidate's basic details from the resume.
RESUME:
{resume}
{format_instructions}
""",
    input_variables=["resume"],
    partial_variables={
        "format_instructions": basic_info_parser.get_format_instructions()
    },
)

class Education(BaseModel):
    qualification: str
    establishment: Optional[str]
    country: Optional[str]
    year: Optional[str]
education_parser = PydanticOutputParser(pydantic_object=Education)
education_prompt = PromptTemplate(
    template="""
Extract the candidate's education details.
RESUME:
{resume}
{format_instructions}
""",
    input_variables=["resume"],
    partial_variables={
        "format_instructions": education_parser.get_format_instructions()
    },
)
class WorkExperience(BaseModel):
    company_name: str
    job_title: str
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

work_experience_parser = PydanticOutputParser(
    pydantic_object=WorkExperience
)
work_experience_prompt = PromptTemplate(
    template="""
Extract one work experience entry from the resume.
RESUME:
{resume}
{format_instructions}
""",
    input_variables=["resume"],
    partial_variables={
        "format_instructions": work_experience_parser.get_format_instructions()
    },
)
class Skills(BaseModel):
    skills: List[str]
    professional_development: Optional[List[str]]
    other: Optional[List[str]]

skills_parser = PydanticOutputParser(pydantic_object=Skills)
skills_prompt = PromptTemplate(
    template="""
Extract:
- Technical skills
- Professional certifications / awards
- Other information (languages, interests, etc.)

RESUME:
{resume}
{format_instructions}
""",
    input_variables=["resume"],
    partial_variables={
        "format_instructions": skills_parser.get_format_instructions()
    },
)
