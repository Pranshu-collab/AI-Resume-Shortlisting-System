from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


class JobBasicInfo(BaseModel):
    job_title: str = Field(description="Title of the job role")
    company_name: Optional[str] = Field(description="Company offering the job")
    location: Optional[str] = Field(description="Job location")
    employment_type: Optional[str] = Field(description="Full-time, Internship, Contract, etc.")


job_basic_info_parser = PydanticOutputParser(
    pydantic_object=JobBasicInfo
)
job_basic_info_prompt = PromptTemplate(
    template="""
Extract the job basic details from the job description.

JOB DESCRIPTION:
{jd_text}

{format_instructions}
""",
    input_variables=["jd_text"],
    partial_variables={
        "format_instructions": job_basic_info_parser.get_format_instructions()
    },
)

class JobSkills(BaseModel):
    required_skills: List[str] = Field(description="Mandatory technical skills required")
    preferred_skills: Optional[List[str]] = Field(description="Preferred or good-to-have skills")

job_skills_parser = PydanticOutputParser(
    pydantic_object=JobSkills
)
job_skills_prompt = PromptTemplate(
    template="""
Extract:
- Required technical skills
- Preferred or good-to-have skills

JOB DESCRIPTION:
{jd_text}

{format_instructions}
""",
    input_variables=["jd_text"],
    partial_variables={
        "format_instructions": job_skills_parser.get_format_instructions()
    },
)
class JobResponsibilities(BaseModel):
    responsibilities: List[str] = Field(description="List of job responsibilities")

job_responsibilities_parser = PydanticOutputParser(
    pydantic_object=JobResponsibilities
)
job_responsibilities_prompt = PromptTemplate(
    template="""
Extract the key job responsibilities.

JOB DESCRIPTION:
{jd_text}

{format_instructions}
""",
    input_variables=["jd_text"],
    partial_variables={
        "format_instructions": job_responsibilities_parser.get_format_instructions()
    },
)

class JobExperience(BaseModel):
    minimum_experience_years: Optional[str] = Field(
        description="Minimum years of experience required"
    )
    experience_description: Optional[str] = Field(
        description="Description of required experience"
    )

job_experience_parser = PydanticOutputParser(
    pydantic_object=JobExperience
)
job_experience_prompt = PromptTemplate(
    template="""
Extract the experience requirements from the job description.

JOB DESCRIPTION:
{jd_text}

{format_instructions}
""",
    input_variables=["jd_text"],
    partial_variables={
        "format_instructions": job_experience_parser.get_format_instructions()
    },
)
