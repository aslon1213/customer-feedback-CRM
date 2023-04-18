import requests

api_url = "https://api.api-ninjas.com/v1/imagetotext"
image_file_descriptor = open("test_photo.jpeg", "rb")
files = {"image": image_file_descriptor}
api_key = "ODkT2TdtPsa07M3VjSpb5g==BtNCfrrlHD38lCSu"
headers = {"X-Api-Key": api_key}
r = requests.post(api_url, files=files, headers=headers)
print(r.json())
