"""AI Client Class"""

from os import environ

from errors import AiResponseError
from src.constants.constants import AI_ROLE_FOR_PROMPT

from httpx import AsyncClient, CookieConflict, HTTPError, InvalidURL, StreamError


class AIClient:
    """
    Class for generating event description by AI. (Claude 3)

    Methods
    -------
    static async generate_event_description()
        Generates event description by requesting Claude 3 with prepared special role.

    """

    @staticmethod
    async def generate_event_description(event_name: str) -> str:
        """
        Generates event description using event name.

        Parameters
        ----------
        event_name : str
            Event name.

        Returns
        -------
        str
            Generated event description.

        Raises
        ------
        AiResponseError
            Raises when AI sent bad response.

        """
        api_key = environ["OPENROUTER_API_KEY"]

        prompt = event_name
        index = (
            1
            if all(
                char.isalpha()
                and (
                    "A" <= char.upper() <= "Z"
                    or not (
                        "A" <= char.upper() <= "Z"
                        or "А" <= char.upper().replace("Ё", "Е") <= "Я"  # noqa: RUF001
                    )
                )
                for char in prompt.replace(" ", "")
            )
            else 0
        )
        async with AsyncClient() as client:
            try:
                response = await client.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                    },
                    json={
                        "model": "anthropic/claude-3-haiku",
                        "messages": [
                            {"role": "system", "content": AI_ROLE_FOR_PROMPT[index]},
                            {
                                "role": "user",
                                "content": ("Опиши ", "Describe ")[index] + prompt,
                            },
                        ],
                    },
                )
                try:
                    return str(response.json()["choices"][0]["message"]["content"])
                except KeyError:
                    raise AiResponseError(
                        ". ".join(
                            str(response.json()["error"]["message"]).split(". ")[:2]
                        )
                    )
            except (HTTPError, InvalidURL, CookieConflict, StreamError) as e:
                raise AiResponseError(e)
