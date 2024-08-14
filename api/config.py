from dotenv import load_dotenv
import os 


load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv('DB_PORT')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_NAME =os.getenv('DB_NAME')