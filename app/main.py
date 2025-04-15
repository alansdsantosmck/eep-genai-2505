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

        # Step 2: Prepare a list to store scored candidates
        scored_candidates = []

        # Step 3: Iterate through each candidate and construct a prompt
        for candidate in candidates:
            # Dynamically construct the full_name field
            full_name = f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip()

            # Debugging log
            print(f"Processing candidate: {full_name}")

            prompt = f"""
            Based on the job description and candidate profile below, evaluate the match and provide a score (0-10) and explanation.
            Return the result in the following JSON format:
            {{
                "full_name": "Candidate Name",
                "score": float,
                "explanation": "Reason for the score"
            }}

            Job Description:
            {request.job.dict()}

            Candidate Profile:
            {candidate}
            """

            # Step 4: Call the OpenAI model using ChatCompletion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that evaluates candidates for job positions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )

            # Extract the content from the OpenAI response
            content = response['choices'][0]['message']['content']
            print(f"Raw OpenAI response for {full_name}: {content}")  # Debugging log

            # Remove Markdown-style code block formatting if present
            if content.startswith("```") and content.endswith("```"):
                content = content.strip("```").strip("json").strip()

            # Safely parse the response content as JSON
            scored_candidate = json.loads(content)
            scored_candidates.append(scored_candidate)

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


@app.post("/match_test", response_model=List[CandidateMatch])
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