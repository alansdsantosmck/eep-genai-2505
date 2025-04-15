def generate_batch_prompt(job, candidates):
    """Generates a prompt that evaluates all candidates in a single request."""
    # TODO: Create a more robust prompt for evaluating multiple candidates against specific job requirements as outlined
    return f"""
    You are an AI assistant evaluating how well candidates match a job description.

    **Job Description**
    Title: {job['title']}

    **Candidates Being Evaluated**
    {candidates}
    """

