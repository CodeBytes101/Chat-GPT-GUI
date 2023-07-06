import openai


def respone_genrator(query: str) -> str:
    openai.api_key = open("api.txt", "r").read()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}]
    )
    return str((dict(((response["choices"])[0])["message"]))["content"])
