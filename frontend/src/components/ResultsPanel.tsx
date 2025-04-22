import React from 'react';
import {
  Typography, Box, Card, CardContent,
  Chip, Divider, Grid, Rating
} from '@mui/material';
import { ResultsPanelProps } from '../types';

const ResultsPanel: React.FC<ResultsPanelProps> = ({ matches }) => {
  return (
    <Box>
      <Typography variant="h5" component="h2" gutterBottom>
        Top Candidate Matches
      </Typography>
      
      <Grid container spacing={3}>
        {matches.map((candidate, index) => (
          <Grid item xs={12} key={index}>
            <Card 
              elevation={2}
              sx={{
                mb: 2,
                border: '1px solid',
                borderColor: index === 0 ? 'primary.main' : 'grey.300',
                bgcolor: index === 0 ? 'primary.light' : 'background.paper',
                '&:hover': {
                  boxShadow: 6,
                }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" component="h3" color={index === 0 ? 'primary.contrastText' : 'inherit'}>
                    {candidate.full_name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" sx={{ mr: 1 }}>
                      Match Score:
                    </Typography>
                    <Rating 
                      value={candidate.score / 2}
                      precision={0.5}
                      readOnly
                    />
                    <Chip 
                      label={`${candidate.score.toFixed(1)}/10`}
                      color={index === 0 ? 'secondary' : 'primary'}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  </Box>
                </Box>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body1" color={index === 0 ? 'primary.contrastText' : 'text.secondary'}>
                  {candidate.explanation}
                </Typography>
                
                {index === 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Chip 
                      label="Top Match" 
                      color="secondary"
                      sx={{ fontWeight: 'bold' }}
                    />
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {matches.length === 0 && (
        <Typography variant="body1" color="text.secondary" align="center">
          No matching candidates found.
        </Typography>
      )}
    </Box>
  );
};

export default ResultsPanel;