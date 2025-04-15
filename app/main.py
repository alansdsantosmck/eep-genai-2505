from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Configura a chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configura a URL base da API OpenAI
openai.api_base = os.getenv("openai_base_url")

# Modelos
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
        # Prompt para o LLM
        prompt = f"""
        Baseado na descrição do trabalho abaixo, avalie e classifique os 3 melhores candidatos:
        {request.job.dict()}
        """

        # Chamada ao modelo da OpenAI usando ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que avalia candidatos para vagas de emprego."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Simulação de resposta
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
        # Captura o erro e retorna uma mensagem de erro 500
        print(f"Erro no endpoint /match: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")