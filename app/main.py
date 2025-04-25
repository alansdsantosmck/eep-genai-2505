from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Verify and set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OpenAI API key is not set. Please check your .env file.")
else:
    logging.info("OpenAI API key loaded successfully.")
openai.api_key = api_key

# Retrieve OpenAI API base URL from .env
openai.api_base = os.getenv("OPENAI_BASE_URL", "https://openai.prod.ai-gateway.quantumblack.com/9e5ad06b-ce78-4233-b6d5-173d778eb7a6/v1")  # Default to OpenAI's public API if not set

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Models
class Job(BaseModel):
    cst_name: str
    client_problem_statement: str
    title: str
    location: str
    industry: str
    required_skills: str
    years_experience: int

class MatchRequest(BaseModel):
    job: Job

class CandidateMatch(BaseModel):
    full_name: str
    score: float
    explanation: str

@app.post("/match", response_model=List[CandidateMatch])
async def match_candidates(request: MatchRequest):
    try:
        # Step 1: Load candidates from a JSON file
        candidates_file = "app/data/candidates.json"
        if not os.path.exists(candidates_file):
            logging.error(f"Candidates file not found: {candidates_file}")
            raise HTTPException(
                status_code=500,
                detail="Candidates file not found. Please ensure 'app/data/candidates.json' exists."
            )

        with open(candidates_file, "r") as f:
            try:
                candidates = json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Error parsing candidates file: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Invalid JSON format in candidates file."
                )

        # Step 2: Construct a prompt for OpenAI
        candidate_profiles = "\n".join(
            f"""
            Candidate {i + 1}:
            Name: {candidate.get('first_name', '')} {candidate.get('last_name', '')}
            Title: {candidate.get('title', 'N/A')}
            Skills: {candidate.get('skills', 'N/A')}
            Experience: {candidate.get('years_experience', 'N/A')} years
            Industry Experience: {candidate.get('industry_experience', 'N/A')}
            Location: {candidate.get('location', 'N/A')}
            """
            for i, candidate in enumerate(candidates)
        )

        prompt = f"""
        Based on the job description below, evaluate and rank the candidates provided. 
        For each candidate, provide a score (0-10) and an explanation for the score.
        Return the results in the following JSON format:
        [
            {{
                "full_name": "Candidate Name",
                "score": float,
                "explanation": "Reason for the score"
            }},
            ...
        ]

        Job Description:
        {request.job.dict()}

        Candidate Profiles:
        {candidate_profiles}
        """

        # Step 3: Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that evaluates candidates for job positions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error communicating with OpenAI API. Please check your API key or request."
            )

        # Step 4: Parse the response
        content = response['choices'][0]['message']['content']
        if content.startswith("```") and content.endswith("```"):
            content = content.strip("```").strip("json").strip()

        try:
            scored_candidates = json.loads(content)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing OpenAI response: {e}")
            raise HTTPException(
                status_code=500,
                detail="Invalid response format from OpenAI. Please check the prompt or the OpenAI API response."
            )

        # Step 5: Return top candidates sorted by score
        return sorted(scored_candidates, key=lambda c: c["score"], reverse=True)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")