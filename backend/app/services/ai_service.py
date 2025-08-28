import base64
import io
from PIL import Image
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class HeritageAIService:
    def __init__(self):
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        self.text_model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        # Define prompts for heritage analysis
        self.image_prompt_template = """
        You are a expert historian and heritage guide. Analyze this image of a heritage site and provide detailed information about it.
        
        Please provide information in the following format:
        
        Name: [Official name of the heritage site]
        Location: [City, Country]
        Historical Period: [When it was built]
        Builder/Creator: [Who built/created it]
        Significance: [Why it's important historically/culturally]
        Architectural Style: [Architectural features and style]
        Current Status: [UNESCO status, conservation status, etc.]
        Interesting Facts: [3-5 interesting facts about the site]
        Nearby Attractions: [Other tourist attractions nearby]
        Best Time to Visit: [Ideal time to visit]
        
        If this is not a recognized heritage site, please politely indicate that and ask for a clearer image or more context.
        
        Image analysis:
        """
        
        self.text_prompt_template = """
        You are a expert historian and heritage guide. Provide comprehensive information about the following heritage site: {heritage_query}
        
        Please provide information in the following format:
        
        Name: [Official name of the heritage site]
        Location: [City, Country]
        Historical Period: [When it was built]
        Builder/Creator: [Who built/created it]
        Significance: [Why it's important historically/culturally]
        Architectural Style: [Architectural features and style]
        History: [Detailed historical background]
        Current Status: [UNESCO status, conservation status, etc.]
        Interesting Facts: [5-7 interesting facts about the site]
        Visitor Information: [Opening hours, entry fees, best time to visit]
        Nearby Attractions: [Other tourist attractions nearby]
        Travel Tips: [Practical advice for visitors]
        
        If this is not a recognized heritage site, please provide information about similar heritage sites or ask for clarification.
        """
    
    def analyze_heritage_image(self, image_data):
        """Analyze heritage site from image using Gemini Vision"""
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Generate content with image and prompt
            response = self.vision_model.generate_content([
                self.image_prompt_template,
                image
            ])
            
            return response.text
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def search_heritage_info(self, query):
        """Get heritage information from text query using Gemini"""
        try:
            prompt = PromptTemplate(
                template=self.text_prompt_template,
                input_variables=["heritage_query"]
            )
            
            formatted_prompt = prompt.format(heritage_query=query)
            
            response = self.text_model([
                HumanMessage(content=formatted_prompt)
            ])
            
            return response.content
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def get_heritage_recommendations(self):
        """Get recommended heritage sites"""
        recommendations = [
            {
                "name": "Taj Mahal",
                "location": "Agra, India",
                "description": "Iconic white marble mausoleum and UNESCO World Heritage Site",
                "image_url": "/assets/images/taj-mahal.jpg"
            },
            {
                "name": "Great Pyramid of Giza",
                "location": "Giza, Egypt",
                "description": "Ancient Egyptian pyramid and the oldest of the Seven Wonders",
                "image_url": "/assets/images/pyramid.jpg"
            },
            {
                "name": "Colosseum",
                "location": "Rome, Italy",
                "description": "Ancient Roman amphitheater and iconic symbol of Imperial Rome",
                "image_url": "/assets/images/colosseum.jpg"
            },
            {
                "name": "Machu Picchu",
                "location": "Cusco, Peru",
                "description": "15th-century Inca citadel high in the Andes Mountains",
                "image_url": "/assets/images/machu-picchu.jpg"
            }
        ]
        return recommendations

# Global AI service instance
ai_service = HeritageAIService()