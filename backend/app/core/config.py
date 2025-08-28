import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME", "indranilsamanta2003")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD", "indu94070@2003")
    MONGODB_CLUSTER: str = os.getenv("MONGODB_CLUSTER", "clusterheritage.aedeqma.mongodb.net")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "heritage_db")
    
    # Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    # App Configuration
    PROJECT_NAME: str = "Heritage Virtual Guide API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    @property
    def MONGODB_URI(self):
        from urllib.parse import quote_plus
        username = quote_plus(self.MONGODB_USERNAME)
        password = quote_plus(self.MONGODB_PASSWORD)
        return f"mongodb+srv://{username}:{password}@{self.MONGODB_CLUSTER}/{self.MONGODB_DATABASE}?retryWrites=true&w=majority&appName=ClusterHeritage"

settings = Settings()