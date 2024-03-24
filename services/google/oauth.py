
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID =os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDIERECT_URL=os.getenv('REDIERECT_URL')

async def get_token(code):
    url = 