import axios from 'axios';
import { Job, CandidateMatch } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const matchCandidates = async (job: Job): Promise<CandidateMatch[]> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/match`, { job });
    return response.data;
  } catch (error) {
    console.error('Error matching candidates:', error);
    throw error;
  }
};