from groq import Groq

from app.core.config import (
    GROQ_API_KEY,
    GROQ_MODEL
)


def get_groq_client():
    """
    Creates and returns an authenticated Groq client.
    """

    if not GROQ_API_KEY:
        raise ValueError(
            "Groq API key is missing. "
            "Configure GROQ_API_KEY in your .env file."
        )

    return Groq(api_key=GROQ_API_KEY)


def generate_completion(system_prompt, user_prompt):
    """
    Sends prompts to the Groq LLM and returns
    the generated response.
    """

    client = get_groq_client()

    try:

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            max_completion_tokens=2048
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Groq returned an empty response."
            )

        return content.strip()

    except Exception as error:

        raise RuntimeError(
            f"Groq API request failed: {error}"
        ) from error
