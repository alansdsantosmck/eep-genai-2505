from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load candidates from the JSON file
CANDIDATES_FILE = os.path.join(os.path.dirname(__file__), "data/candidates.json")

def load_candidates():
    """Loads candidates from a JSON file."""
    with open(CANDIDATES_FILE, "r") as file:
        return json.load(file)

def evaluate_candidates(job):
    """Evaluates all candidates using a SINGLE OpenAI API request."""
    candidates = load_candidates()

    # Make a single OpenAI API call with a detailed prompt to get candidate evaluations 
    response = ""

    # Parse the LLM response
    result_text = response.strip()
    results = parse_batch_response(result_text)

    return results

def parse_batch_response(response_text: str):
    """Parses the batch response and extracts scores and explanations for all candidates."""
    results = []

    # 1. Leverage regex to handle varying spaces and multi-line explanations when getting the candidates, their scores, and explanations

    # 2. Append each candidate's names, score, and explanation to the results list

    # 3. Sort candidates by score in descending order

    # 4. Return only the top 3 candidates

    return results



