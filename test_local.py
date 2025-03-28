
import requests


try:
    response = requests.post("http://localhost:8000/", json={"Country": "Zimbabwe", "Date":"2005"})

    if response.status_code == 200:
        print("yup")
        print(response.text)
    else:
        print(f"Error code {response.status_code} : {response.reason}")
except Exception as e:
    print("Error", e)


