import json
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def extract(resume_p,job_desc_p):
    try:
        with open(resume_p,'r',encoding='utf-8') as file:
            r_data=json.load(file)
    except FileNotFoundError:
        print("Error:File resume_p not found")
    except json.JSONDecodeError:
        print("Error:File resume_p couldn't be decoded")
    try:
        with open(job_desc_p,'r',encoding='utf-8') as file:
            j_data=json.load(file)
    except FileNotFoundError:
        print("Error:File job_desc_p not found")
    except json.JSONDecodeError:
        print("Error:File job_desc_p couldn't be decoded")
    return r_data,j_data
def exact_score(r_data,j_data):
    
    def normalize(text):
       text = text.lower()
       text = re.sub(r'[^a-z0-9\s]', ' ', text)
       return re.sub(r'\s+', ' ', text).strip()
    def column_to_text(data):
       if isinstance(data, list):
         return " ".join(map(str, data))
       elif isinstance(data, dict):
         return " ".join(map(str, data.values()))
       else:
         return str(data)
    def exact_column_match(jd_column, resume_column):

       jd_text = normalize(column_to_text(jd_column))
       resume_text = normalize(column_to_text(resume_column))

       jd_words = set(jd_text.split())
       resume_words = set(resume_text.split())

       if not jd_words:
         return {
            "score": 0,
            "matched_words": [],
            "missing_words": []
        }
       matched = jd_words.intersection(resume_words)
       missing = jd_words - matched

       score = (len(matched) / len(jd_words)) * 100

       return {
        "score": round(score, 2),
        "matched_words": list(matched),
        "missing_words": list(missing)
      }
       
    weights = {
        "skills": 0.3,
        "professional_experience": 0.3,
        "projects": 0.2,
        "education": 0.1,
        "certifications": 0.1
    }
    results = {}
    final_score = 0

    for column, weight in weights.items():
        if column in j_data and column in r_data:

            column_result = exact_column_match(
                j_data[column],
                r_data[column]
            )
            results[column] = column_result
            final_score += column_result["score"] * weight

        else:
            results[column] = {
                "score": 0,
                "matched_words": [],
                "missing_words": []
            }
    results["final_score"] = round(final_score, 2)
    return round(final_score,2)

def similarity_score(r_data,j_data):
      model = SentenceTransformer('all-MiniLM-L6-v2')
      def structured_to_text(data):
       full_text = []
    
       for key, value in data.items():
          if isinstance(value, list):
            full_text.append(" ".join(map(str, value)))
          elif isinstance(value, dict):
            full_text.append(" ".join(map(str, value.values())))
          else:
            full_text.append(str(value))
    
       return " ".join(full_text) 

      jd_text = structured_to_text(j_data)
      resume_text = structured_to_text(r_data)
      jd_embedding = model.encode(jd_text)
      resume_embedding = model.encode(resume_text)
      similarity = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
     )[0][0]

      return round(similarity * 100, 2)

def ownership_score(resume_data):
    OWNERSHIP_KEYWORDS = ["led","lead","managed","manage","owned","own","built","build","architected","designed",
"initiated","spearheaded","coordinated","implemented","developed","directed","created","launched","driven","responsible"
]
    def normalize(text):
      text = text.lower()
      text = re.sub(r'[^a-z0-9\s]', ' ', text)
      return re.sub(r'\s+', ' ', text).strip()
    def experience_to_text(resume_data):

      experience = resume_data.get("professional_experience", "")

      if isinstance(experience, list):
        return " ".join(map(str, experience))
      elif isinstance(experience, dict):
        return " ".join(map(str, experience.values()))
      else:
        return str(experience)
    experience_text = normalize(experience_to_text(resume_data))

    words = experience_text.split()
    total_words = len(words)

    if total_words == 0:
        return {
            "score": 0,
            "ownership_terms_found": []
        }

    found_terms = []
    count = 0

    for word in words:
        if word in OWNERSHIP_KEYWORDS:
            count += 1
            found_terms.append(word)

    raw_score = count / total_words
    scaled_score = min(raw_score * 500, 100)  
    return round(scaled_score, 2)

def achievement_score(resume_data):
    ACHIEVEMENT_VERBS = [
    "increased", "reduced", "improved", "optimized",
    "boosted", "enhanced", "accelerated", "grew",
    "expanded", "generated", "achieved", "delivered",
    "launched", "won", "awarded", "patented",
    "published", "outperformed", "saved"
]
    # Percentage pattern (20%, 35 percent)
    PERCENT_PATTERN = r"\b\d+(\.\d+)?\s?%|\b\d+(\.\d+)?\s?(percent)"

    # Number pattern (1000, 3x, 2.5x)
    NUMBER_PATTERN = r"\b\d+(\.\d+)?x?\b"
    def normalize(text):
      text = text.lower()
      text = re.sub(r'[^a-z0-9\s%]', ' ', text)
      return re.sub(r'\s+', ' ', text).strip()
    def experience_to_text(resume_data):
      experience = resume_data.get("professional_experience", "")

      if isinstance(experience, list):
        return " ".join(map(str, experience))
      elif isinstance(experience, dict):
        return " ".join(map(str, experience.values()))
      else:
        return str(experience)
    text = normalize(experience_to_text(resume_data))
    percentages = re.findall(PERCENT_PATTERN, text)
    numbers = re.findall(NUMBER_PATTERN, text)
    words = text.split()
    verbs_found = [word for word in words if word in ACHIEVEMENT_VERBS]
  
    percent_score = len(percentages) * 3
    number_score = len(numbers) * 1
    verb_score = len(verbs_found) * 2
    raw_score = percent_score + number_score + verb_score
    # Normalize to 0–100
    scaled_score = min(raw_score * 5, 100)

    return round(scaled_score, 2)
        
