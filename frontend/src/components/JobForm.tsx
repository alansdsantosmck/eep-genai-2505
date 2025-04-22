import React, { useState } from 'react';
import {
  TextField, Button, Grid, Typography, 
  InputAdornment, Box, CircularProgress
} from '@mui/material';
import { Job, JobFormProps } from '../types';

const JobForm: React.FC<JobFormProps> = ({ onSubmit, loading }) => {
  const initialJobState: Job = {
    cst_name: '',
    client_problem_statement: '',
    title: '',
    location: '',
    industry: '',
    required_skills: '',
    years_experience: 0
  };

  const [job, setJob] = useState<Job>(initialJobState);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    let isValid = true;

    if (!job.cst_name.trim()) {
      newErrors.cst_name = 'Customer name is required';
      isValid = false;
    }

    if (!job.client_problem_statement.trim()) {
      newErrors.client_problem_statement = 'Problem statement is required';
      isValid = false;
    }

    if (!job.title.trim()) {
      newErrors.title = 'Job title is required';
      isValid = false;
    }

    if (job.years_experience < 0) {
      newErrors.years_experience = 'Years of experience must be positive';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setJob(prev => ({
      ...prev,
      [name]: name === 'years_experience' ? Number(value) : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(job);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Typography variant="h5" component="h2" gutterBottom>
        Job Description
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Customer Name"
            name="cst_name"
            value={job.cst_name}
            onChange={handleChange}
            error={!!errors.cst_name}
            helperText={errors.cst_name || ''}
            disabled={loading}
            margin="normal"
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Job Title"
            name="title"
            value={job.title}
            onChange={handleChange}
            error={!!errors.title}
            helperText={errors.title || ''}
            disabled={loading}
            margin="normal"
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Problem Statement"
            name="client_problem_statement"
            value={job.client_problem_statement}
            onChange={handleChange}
            error={!!errors.client_problem_statement}
            helperText={errors.client_problem_statement || ''}
            disabled={loading}
            margin="normal"
            multiline
            rows={4}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Industry"
            name="industry"
            value={job.industry}
            onChange={handleChange}
            disabled={loading}
            margin="normal"
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Location"
            name="location"
            value={job.location}
            onChange={handleChange}
            disabled={loading}
            margin="normal"
          />
        </Grid>
        
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Required Skills"
            name="required_skills"
            value={job.required_skills}
            onChange={handleChange}
            disabled={loading}
            margin="normal"
            multiline
            rows={3}
            placeholder="Enter required skills separated by commas"
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="number"
            label="Years of Experience"
            name="years_experience"
            value={job.years_experience}
            onChange={handleChange}
            error={!!errors.years_experience}
            helperText={errors.years_experience || ''}
            disabled={loading}
            margin="normal"
            InputProps={{
              endAdornment: <InputAdornment position="end">years</InputAdornment>,
              inputProps: { min: 0 }
            }}
          />
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          disabled={loading}
        >
          {loading ? (
            <>
              <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
              Matching...
            </>
          ) : (
            'Find Matching Candidates'
          )}
        </Button>
      </Box>
    </form>
  );
};

export default JobForm;