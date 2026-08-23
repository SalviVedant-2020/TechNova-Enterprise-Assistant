def clean_sql(response: str) -> str:
    return (
        response.replace("```sql", "")
                .replace("```", "")
                .strip()
    )