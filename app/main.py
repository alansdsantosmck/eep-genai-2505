from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Configure the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure the OpenAI API base URL
openai.api_base = os.getenv("openai_base_url")

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
        # Prompt for the LLM
        prompt = f"""
        Based on the job description below, evaluate and rank the top 3 candidates:
        {request.job.dict()}
        """

        # Call the OpenAI model using ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that evaluates candidates for job positions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Simulated response
        matches = [
            {
                "full_name": "Tammy Harvey",
                "score": 8.0,
                "explanation": "Has the required skills including Python and PostgreSQL, and 5 years of experience which matches the job's requirements. E-Commerce industry experience is relevant to the tech industry."
            },
            {
                "full_name": "Martin Crane",
                "score": 7.0,
                "explanation": "Has experience with Python and PostgreSQL, and is located in New York which is a plus for location fit. However, lacks experience with FastAPI and Data Pipelines specifically."
            },
            {
                "full_name": "Kyle Mclaughlin",
                "score": 7.0,
                "explanation": "Possesses Python and PostgreSQL skills with 10 years of experience in relevant industries, but lacks specific experience with FastAPI and Data Pipelines."
            }
        ]

        return matches

    except Exception as e:
        # Capture the error and return a 500 error message
        print(f"Error in /match endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")