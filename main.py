from openai import OpenAI
client = OpenAI(api_key="sk-BXIUJfFqAg1XqqTW7o5tQK9YyhyPQbwdNt9sMm4RIZuiStaW",base_url="https://api.chatanywhere.cn")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response)