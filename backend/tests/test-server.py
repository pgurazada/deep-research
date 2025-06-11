import requests

local_url = "http://127.0.0.1:8000/answer"

# local testing
response = requests.post(
    local_url,
    json={"text": "Is starlink available in the UK?"}
)

print(response.json())