import argparse
import json
import os
import sys
import logging
from copy import deepcopy
from pathlib import Path

import docx
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from resume_pydantic_models_prompts import (
    BasicInfo,
    basic_info_parser,
    basic_details_prompt,
    Education,
    education_parser,
    education_prompt,
    WorkExperience,
    work_experience_parser,
    work_experience_prompt,
    Skills,
    skills_parser,
    skills_prompt
)

from utils import output_template,extract_emails,extract_github_and_linkedin_urls

load_dotenv()
api_key = os.getenv("key_1_to_test")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class ResumeManager:
    def __init__(self, resume_f, model_name="gpt-4o-mini"):
        logging.info("Initializing ResumeManager")

        self.output = deepcopy(output_template)
        self.resume = get_resume_content(resume_f)

        self.model = ChatOpenAI(
            model=model_name,
            temperature=0
        )

    def run_parser(self, prompt_template, parser):
        formatted_prompt = prompt_template.format(resume=self.resume)

        logging.info("Querying LLM for structured extraction")

        response = self.model.invoke(formatted_prompt)

        return parser.parse(response.content)

    def process_file(self):
        self.extract_basic_info()
        self.extract_education()
        self.extract_work_experience()
        self.extract_skills()

    def extract_basic_info(self):
        parsed = self.run_parser(basic_details_prompt, basic_info_parser)

        self.output["candidate_name"] = parsed.name
        self.output["job_title"] = parsed.job_title
        self.output["bio"] = parsed.bio
        self.output["contact_info"]["location"] = parsed.location
        self.output["contact_info"]["phone_number"] = parsed.phone

        emails = extract_emails(self.resume)
        urls = extract_github_and_linkedin_urls(self.resume)

        if emails:
          self.output["contact_info"]["email_address"] = emails[0]
        self.output["contact_info"]["personal_urls"] = urls

    def extract_education(self):
        parsed = self.run_parser(education_prompt, education_parser)
        self.output["education"] = parsed.dict()

    def extract_work_experience(self):
        parsed = self.run_parser(work_experience_prompt, work_experience_parser)
        self.output["work_experience"] = parsed.dict()

    def extract_skills(self):
        parsed = self.run_parser(skills_prompt, skills_parser)

        self.output["skills"] = parsed.skills
        self.output["professional_development"] = parsed.professional_development
        self.output["other"] = parsed.other


def get_resume_content(file_path):
    extension = os.path.splitext(file_path)[1]

    if extension == ".pdf":
        pdf_reader = PdfReader(file_path)
        content = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                content += text + "\n"

    elif extension in [".docx", ".doc"]:
        doc = docx.Document(file_path)
        content = "\n".join(p.text for p in doc.paragraphs)

    else:
        sys.exit(f"Unsupported file type {extension}")

    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Resume using LLM")
    parser.add_argument("file_path")
    parser.add_argument("--model_name", default="gpt-4o-mini")

    args = parser.parse_args()

    manager = ResumeManager(args.file_path, args.model_name)
    manager.process_file()

    resume_name = Path(args.file_path).stem
    output_file_path = f"{resume_name}_parsed.json"

    with open(output_file_path, "w") as f:
        json.dump(manager.output, f, indent=2)

    print(json.dumps(manager.output, indent=2))
