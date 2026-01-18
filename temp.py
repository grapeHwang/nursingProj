from google import genai
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

scopes = ['https://www.googleapis.com/auth/cloud-platform']
        
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=scopes)

client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location="global", #os.getenv("GOOGLE_CLOUD_LOCATION"),
    credentials=credentials
)

for model in client.models.list():
    if "flash" in model.name:
        print(model.name) 