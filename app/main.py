from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv
import json  # Import the JSON module for safe parsing


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
        # Step 1: Load candidates from a JSON file
        with open("app/data/candidates.json", "r") as f:
            candidates = json.load(f)

        # Step 2: Construct a single prompt with all candidate profiles
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

        # Step 3: Call the OpenAI model using ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that evaluates candidates for job positions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500  # Adjust max_tokens based on the size of the input
        )

        # Step 4: Extract and parse the response
        content = response['choices'][0]['message']['content']
        print(f"Raw OpenAI response: {content}")  # Debugging log

        # Remove Markdown-style code block formatting if present
        if content.startswith("```") and content.endswith("```"):
            content = content.strip("```").strip("json").strip()

        # Safely parse the response content as JSON
        scored_candidates = json.loads(content)

        # Step 5: Sort candidates by score in descending order
        top_candidates = sorted(scored_candidates, key=lambda c: c["score"], reverse=True)[:3]

        return top_candidates

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"JSON parsing error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Invalid response format from OpenAI. Please check the prompt or the OpenAI API response."
        )
    except Exception as e:
        # Capture other errors and return a 500 error message
        print(f"Error in /match endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")