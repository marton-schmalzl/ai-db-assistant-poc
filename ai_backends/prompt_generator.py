def generate_prompt(schema, prompt, history=None):
    """
    Generates a prompt string from the schema, prompt, and conversation history using a unified template.

    Args:
        schema (str): The database schema.
        prompt (str): The user question.
        history (list): A list of tuples, where each tuple contains the user's question and the AI's response.

    Returns:
        str: The generated prompt string.
    """
    template = f"""
        **IMPORTANT and CRITICAL INSTRUCTION**: Generate a valid SQL query with comments to answer the question based **EXCLUSIVELY** on the provided database schema.
        Your SQL query **MUST ONLY** use tables and columns that are **explicitly defined** in the provided schema.
        **ABSOLUTELY DO NOT** use any tables or columns that are **NOT** present in the schema.
        Ensure that all information is retrieved from the **correct tables** as defined in the schema. Use JOINs and aggregations when necessary.
        It is **ABSOLUTELY CRITICAL** to pay meticulous attention to the schema and column names. 
        **Column names are case-sensitive**. Your generated SQL query **MUST ALSO BE case-sensitive** and accurately reflect the schema's case.
        To reiterate, **UNDER NO CIRCUMSTANCES** should you invent or assume the existence of tables or columns that are not in the provided schema.
        Return **ONLY** the raw SQL query, without any markdown wrappers, as plain text.

        Database Schema:
        {schema}

        This prompt includes history from previous turns of conversation.
        """

    if history:
        for user_question, ai_response in history:
            template += f"""
        Question:
        {user_question}

        SQL Query:
        {ai_response}
        """

    template += f"""
        Question:
        {prompt}

        SQL Query:
        """
    return template
