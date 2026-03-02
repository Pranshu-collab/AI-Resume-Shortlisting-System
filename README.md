# AI Resume Shortlisting & Job Description Matching System
## Technical Architecture & Design Report
### 1. System Overview
This system is designed to:
- Parse a candidate’s resume using LLM-based structured extraction
- Parse a job description using the same structured methodology
- Convert both into comparable structured formats
- Compute multiple evaluation scores
- Display results through a Streamlit application
- The architecture is modular, extensible, and designed for partial automation of recruitment evaluation.

### 2. Resume Parsing Architecture
#### 2.1 Why LangChain Was Used
LangChain was chosen for:
- Structured LLM output handling
- Prompt templating
- Output parsing via Pydantic
- Model abstraction layer
- Easy integration with OpenAI models
- Instead of using raw API calls, LangChain provides:
- Prompt → Model → Structured Output pipeline
- Clean separation between logic and schema
- Automatic validation of model responses
- This makes the system more robust and production-aligned.

#### 2.2 Resume Parsing Logic
The resume parsing system follows this pipeline:
- PDF Upload
- Text Extraction
- Prompt Construction
- LLM Structured Extraction
- Pydantic Validation
- JSON Output Storage

#### 2.3 Prompt Engineering Design
The prompts were written with section-wise clarity to ensure accurate extraction.
Instead of asking for a generic summary, the model was explicitly instructed to extract:
- Work Experience
- Skills
- Education
- Projects
- Certifications
- Achievements
- Contact Information
Why Structured Section Prompts?
- LLMs hallucinate less when:
- Given structured instructions
- Asked for specific keys
- Given schema constraints
The prompt design ensured:
- Clear role instruction (You are an expert resume parser)
- Explicit JSON output format
- Strict instructions to not invent data
- Handling missing fields gracefully
Each section was logically separated inside the prompt to improve accuracy.

#### 2.4 Pydantic Schema Design
Pydantic was used to define:
- Work Experience model
- Education model
- Skill lists
- Achievement fields
- Ownership-related statements
Why Pydantic?
- Automatic validation
- Structured parsing from LLM output
- Type enforcement
- Fail-safe against malformed JSON
This ensures:
- Output consistency
- Easier downstream scoring
- Reliable schema alignment with job description parser

#### 2.5 Threading & Fallback Strategy
Both resume and job description parsing can be parallelized.
Why Threading?
- Resume parsing and JD parsing are independent tasks.
- They can be executed concurrently.
- Improves latency.
- Scales well in production.
Fallback Logic
Fallback mechanisms were considered for:
- LLM failure
- JSON parsing errors
- Timeout issues
- Partial extraction
Fallback approach includes:
- Retry with reduced temperature
- Retry with simplified prompt
- Return partial structured output if full extraction fails
- This increases robustness in real-world scenarios.

### 3. Job Description Parsing Architecture
The job description parser mirrors the resume parser structure.
#### 3.1 Why Same Architecture?
Consistency.
If resume and job description are parsed differently:
- Score computation becomes unreliable
- Field alignment becomes inconsistent
Therefore:
- Same LangChain pipeline
- Same Pydantic schema format
- Similar prompt structure
- Minor logical adjustments
  
#### 3.2 Differences from Resume Parser
While the logic is similar, differences include:
- Focus on required skills instead of possessed skills
- Extraction of required experience level
- Mandatory vs preferred skills
- Role responsibilities
- Qualification requirements
The prompt was adjusted to:
- Extract requirements instead of achievements
- Identify must-have vs good-to-have skills
- Capture seniority level indicators

### 4. Scoring Architecture
After structured extraction, the system moves to scoring.
The scoring module receives:
- Resume structured data
- Job description structured data
- It then computes multiple evaluation metrics.
#### 4.1 Exact Match Score
Logic:
- Extract comparable fields (skills, tools, technologies)
- Normalize text (lowercase, strip whitespace)
- Count overlapping words between resume and job description
- Compute ratio-based score
Purpose:
- Measures direct keyword alignment.
- Strength:
- Fast
- Deterministic
- Interpretable
- Limitation:
- Cannot capture semantic similarity

#### 4.2 Semantic Similarity Score
For semantic similarity, Sentence Transformers were used.
Definition:
Sentence Transformers are deep learning models that generate dense vector embeddings for text such that semantically similar texts have similar vector representations.
Process:
- Convert resume skill phrases into embeddings
- Convert JD skill phrases into embeddings
- Compute cosine similarity
- Aggregate similarity score
Why Sentence Transformers?
- Captures contextual similarity
- Handles synonyms
- Goes beyond exact word match
- Better for modern NLP evaluation
- This makes the system intelligent rather than purely keyword-based.

#### 4.3 Achievement Score
Achievement score is calculated using regex-based detection.
Logic:
- Identify quantifiable impact phrases
- Detect numbers followed by performance verbs
- Patterns like:
- Increased revenue by X%
- Reduced cost by X%
- Improved performance by X%
- Regex was used to detect:
- Numeric patterns
- Percentage improvements
- Performance-related verbs
Purpose:
Measures impact-driven experience.

#### 4.4 Ownership Score
Ownership score identifies:
Leadership verbs
Initiative-driven phrases
Words like:
- Led
- Built
- Designed
- Developed
- Implemented
This measures:
- Responsibility level
- Initiative
- Leadership exposure
Unlike achievement score (impact-based), ownership score measures authority and control.

### 5. Utilities Module (utils.py)
The utilities module contains:
- Shared schema definitions
- Common data formatting functions
- Helper normalization functions
- Output structure alignment
Purpose:
- Avoid duplication
- Centralize output schema
- Maintain consistent data structure
- Improve maintainability
- This ensures both parsers produce identical structured outputs.

### 6. Streamlit Application (app.py)
The Streamlit app acts as the frontend + backend controller.
Responsibilities:
- Accept resume PDF
- Accept job description PDF
- Trigger parsing managers
- Compute scores
- Display structured outputs
- Display evaluation metrics
- Measure execution time
Why Streamlit?
- Rapid prototyping
- Interactive UI
- Easy deployment
- Minimal frontend overhead
The app orchestrates the full pipeline:
Upload → Parse → Score → Display

### 7. Running the System
#### Step 1: Clone or Download Project
- Download the entire project directory.
#### Step 2: Create Virtual Environment
- Inside project folder:
- Create virtual environment
- Activate it
#### Step 3: Install Requirements
- Install all dependencies using:
- requirements.txt
This includes:
- streamlit
- langchain
- openai
- pydantic
- sentence-transformers
- PyPDF
- other NLP utilities
#### Step 4: Add OpenAI API Key
- After generating a new API key:
- Store it securely:
- Option 1:
- Environment variable
- Option 2:
- .env file
- The key is used inside:
- Resume parser (LLM initialization)
- Job description parser
- Never hardcode the key inside source files.
#### Step 5: Run the Application
- Activate virtual environment.
- Run:
- streamlit run app.py
- Streamlit will generate a local URL.
- Open in browser.
- Upload resume + job description.
- View structured output + scores.

### 8. Architectural Strengths
- Modular
- Scalable
- Structured output driven
- LLM + deterministic scoring hybrid
- Extensible scoring framework
- Production-ready design foundation

### 9. AI-Assisted Development
AI tools were used to:
- Simplify prompt engineering
- Accelerate structured schema writing
- Improve regex pattern design
- Optimize scoring logic
- Refactor repetitive components
- Improve modular design
The use of AI:
- Reduced development time
- Improved code consistency
- Helped explore better architectural patterns
- Assisted in debugging integration issues
However:
- All architectural decisions were manually reasoned
- Design logic was consciously structured
- Validation and system flow were carefully reviewed
- AI acted as an accelerator, not a replacement for system design thinking.
