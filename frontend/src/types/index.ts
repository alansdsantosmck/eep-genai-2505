export interface Job {
  cst_name: string;
  client_problem_statement: string;
  title: string;
  location: string;
  industry: string;
  required_skills: string;
  years_experience: number;
}

export interface CandidateMatch {
  full_name: string;
  score: number;
  explanation: string;
}

export interface JobFormProps {
  onSubmit: (job: Job) => void;
  loading: boolean;
}

export interface ResultsPanelProps {
  matches: CandidateMatch[];
}