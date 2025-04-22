import React, { useState } from 'react';
import { 
  Container, CssBaseline, ThemeProvider, createTheme, 
  Box, Typography, Paper 
} from '@mui/material';
import JobForm from './components/JobForm';
import ResultsPanel from './components/ResultsPanel';
import { CandidateMatch, Job } from './types';
import { matchCandidates } from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

const App: React.FC = () => {
  const [matches, setMatches] = useState<CandidateMatch[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleJobSubmit = async (job: Job) => {
    setLoading(true);
    setError(null);
    try {
      const results = await matchCandidates(job);
      setMatches(results);
    } catch (err) {
      setError('Failed to match candidates. Please try again.');
      console.error('Error matching candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            AI-Powered Candidate Matching
          </Typography>
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <JobForm onSubmit={handleJobSubmit} loading={loading} />
          </Paper>
          {matches.length > 0 && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <ResultsPanel matches={matches} />
            </Paper>
          )}
          {error && (
            <Paper elevation={3} sx={{ p: 2, mt: 2, bgcolor: 'error.light' }}>
              <Typography color="error">{error}</Typography>
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default App;