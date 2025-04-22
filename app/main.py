from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json  # Import the JSON module for safe parsing
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import random  # Adicionado para gerar resultados simulados

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Adicionar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Permitir o frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
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
        with open("app/data/candidates.json", "r") as f:
            candidates = json.load(f)
            
        # Em vez de usar a API OpenAI, vamos implementar um sistema de pontuação local simples
        # para encontrar candidatos correspondentes com base em palavras-chave e critérios
        
        job_title_keywords = request.job.title.lower().split()
        job_skills_keywords = [s.strip().lower() for s in request.job.required_skills.split(",")]
        job_location = request.job.location.lower()
        job_industry = request.job.industry.lower()
        job_years = request.job.years_experience
        
        # Lista para armazenar candidatos pontuados
        scored_candidates = []
        
        # Avaliar cada candidato
        for candidate in candidates:
            score = 0
            reasons = []
            
            # Verificar correspondência de título
            candidate_title = candidate.get('title', '').lower()
            if any(keyword in candidate_title for keyword in job_title_keywords):
                title_points = 2
                score += title_points
                reasons.append(f"Job title match (+{title_points})")
            
            # Verificar correspondência de habilidades
            candidate_skills = candidate.get('skills', '').lower()
            matching_skills = [skill for skill in job_skills_keywords if skill in candidate_skills]
            if matching_skills:
                skill_points = len(matching_skills) * 1.5
                score += skill_points
                reasons.append(f"{len(matching_skills)} matching skills (+{skill_points})")
            
            # Verificar correspondência de localização
            candidate_location = candidate.get('location', '').lower()
            if job_location in candidate_location or candidate_location in job_location:
                location_points = 1.5
                score += location_points
                reasons.append(f"Location match (+{location_points})")
            
            # Verificar experiência na indústria
            candidate_industry = candidate.get('industry_experience', '').lower()
            if job_industry in candidate_industry:
                industry_points = 2
                score += industry_points
                reasons.append(f"Industry experience (+{industry_points})")
            
            # Verificar anos de experiência
            candidate_years = candidate.get('years_experience', 0)
            years_diff = abs(candidate_years - job_years)
            if years_diff <= 2:
                years_points = 2
                score += years_points
                reasons.append(f"Years of experience within target range (+{years_points})")
            elif years_diff <= 4:
                years_points = 1
                score += years_points
                reasons.append(f"Years of experience close to target range (+{years_points})")
            
            # Normalizar pontuação para escala de 0 a 10
            normalized_score = min(10, score)
            
            # Adicionar um pouco de variação para evitar empates exatos
            normalized_score = round(normalized_score + random.uniform(-0.3, 0.3), 1)
            normalized_score = max(0, min(10, normalized_score))
            
            # Criar explicação e adicionar candidato à lista
            explanation = "This candidate " + ", ".join(reasons).lower() + "."
            
            full_name = f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}"
            scored_candidates.append({
                "full_name": full_name,
                "score": normalized_score,
                "explanation": explanation
            })
        
        # Ordenar candidatos por pontuação em ordem decrescente
        top_candidates = sorted(scored_candidates, key=lambda c: c["score"], reverse=True)[:3]
        
        return top_candidates

    except Exception as e:
        # Capturar outros erros e retornar uma mensagem de erro 500
        print(f"Error in /match endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")