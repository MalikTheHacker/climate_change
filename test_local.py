import requests



response = requests.post(
    "http://localhost:8000/", 
    json={"Country": "United Arab Emirates", "Date": "2025-01-01"}  # Format date correctly
)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Error code {response.status_code} : {response.reason}")
    print(response.text)  # Print the response content to see error details


