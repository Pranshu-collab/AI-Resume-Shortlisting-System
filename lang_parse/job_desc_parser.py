import argparse
import json
import logging
from copy import deepcopy
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from job_desc_pydantic_prompts import (
    JobBasicInfo,
    job_basic_info_parser,
    job_basic_info_prompt,
    JobSkills,
    job_skills_parser,
    job_skills_prompt,
    JobResponsibilities,
    job_responsibilities_parser,
    job_responsibilities_prompt,
    JobExperience,
    job_experience_parser,
    job_experience_prompt,
)

load_dotenv()
api_key = os.getenv("key_1_to_test")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class JobDescriptionManager:
    def __init__(self, jd_file, model_name="gpt-4o-mini"):
        logging.info("Initializing JobDescriptionManager")

        self.output = {}
        self.jd_text = self.read_jd(jd_file)

        self.model = ChatOpenAI(
            model=model_name,
            temperature=0
        )

    def run_parser(self, prompt_template, parser):
        formatted_prompt = prompt_template.format(jd_text=self.jd_text)

        logging.info("Querying LLM for structured JD extraction")

        response = self.model.invoke(formatted_prompt)

        return parser.parse(response.content)

    def process_file(self):
        self.extract_basic_info()
        self.extract_skills()
        self.extract_responsibilities()
        self.extract_experience()

    def extract_basic_info(self):
        parsed = self.run_parser(job_basic_info_prompt, job_basic_info_parser)
        self.output["basic_info"] = parsed.dict()

    def extract_skills(self):
        parsed = self.run_parser(job_skills_prompt, job_skills_parser)
        self.output["skills"] = parsed.dict()

    def extract_responsibilities(self):
        parsed = self.run_parser(
            job_responsibilities_prompt,
            job_responsibilities_parser
        )
        self.output["responsibilities"] = parsed.dict()

    def extract_experience(self):
        parsed = self.run_parser(
            job_experience_prompt,
            job_experience_parser
        )
        self.output["experience_requirements"] = parsed.dict()

    def read_jd(self, file_path):
        logging.info(f"Reading job description file: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Job Description using LLM")
    parser.add_argument("file_path")
    parser.add_argument("--model_name", default="gpt-4o-mini")

    args = parser.parse_args()

    manager = JobDescriptionManager(args.file_path, args.model_name)
    manager.process_file()

    jd_name = Path(args.file_path).stem
    output_file_path = f"{jd_name}_parsed.json"

    with open(output_file_path, "w") as f:
        json.dump(manager.output, f, indent=2)

    print(json.dumps(manager.output, indent=2))
