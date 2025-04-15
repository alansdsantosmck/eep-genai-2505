from typing import Optional
from pydantic import BaseModel
from datetime import date


class JobRequest(BaseModel):
    cst_name: str
    client_problem_statement: str
    # TODO: Complete the JobRequest model with the required fields


class MatchRequest(BaseModel):
    job: JobRequest  # Ensure this matches the frontend request structure


class CandidateSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    title: str
    skills: str
    is_staffed: bool
    staffing_end_date: Optional[date] = None
    years_experience: int
    industry_experience: str
    location: str


class Config:
    orm_mode = True  # Important! Enables ORM compatibility


# TODO: Create the MatchResult model with the required fields to represent the candidate evaluation results
