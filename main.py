import os
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv

# local packages

from features import sendemail

load_dotenv()

download_youtube_thumbnail_function = {
    "name": "download_youtube_thumbnail",
    "description": "Downloads the thumbnail image of a specified YouTube video and optionally sends it to an email address, which will be provided by the user, if any of the  information required is not present you should tell that user with humorous way :)",
    "parameters": {
        "type": "object",
        "properties": {
            "video_url": {
                "type": "string",
                "description": "The URL of the YouTube video.",
            },
            "resolution": {
                "type": "string",
                "enum": ["default", "mqdefault", "hqdefault", "sddefault", "maxresdefault"],
                "description": "The desired resolution of the thumbnail. Options are 'default' (120x90), 'medium' (320x180), 'high' (480x360), 'standard' (640x480), and 'maxres' (1280x720).",
            },
            "save_path": {
                "type": "string",
                "description": "The full path (including filename) where the thumbnail image will be saved.",
            },
            "send_to_email": {
                "type": "boolean",
                "description": "Indicates whether the downloaded thumbnail should be sent via email. Set this to 'true' only if the user explicitly requests to send the thumbnail through email."
            },
            "recipient_email": {
                "type": "string",
                "description": "The email address to send the thumbnail to. This field is required if 'send_to_email' is set to 'true'."
            }
        },
        "required": ["video_url", "resolution", "save_path"],
    },
}

def call_function(name,**args):
    return functions[name](**args)

user_input = input("Hi there! I'm Your Youtube assistant What I can do for You?\n")

def send_email(recipient_email):
    print(f"working.... email was send to {recipient_email}")

def download_youtube_thumbnail(video_url : str,resolution : str, save_path="thubnail.jpg",send_to_email=False,recipient_email="a@a.com")-> str:

    # https://www.youtube.com/watch?v=Qu2GhmOGgfY

    video_id = video_url.split("?v=")[-1]
    
    download_url = f"https://img.youtube.com/vi/{video_id}/{resolution}.jpg"

    res = requests.get(download_url)
    print(res.status_code)
    if res.status_code==200:
        directory_path = "thumbnails"
        os.makedirs(directory_path, exist_ok=True)

        with open(f"thumbnails/{save_path}.jpg","wb") as img :
            img.write(res.content)
        
        print(f"{video_url} Thumbnail Was Downloaded Succefully!")

    if send_to_email:
        sender_email = os.getenv("sender_email")
        sender_password = os.getenv("sender_password")
        attachment = f"{save_path}.jpg" 
        
        sendemail(sender_email=sender_email,sender_passoword=sender_password,reciever_email=recipient_email,attachment=attachment)
    
    return f""

functions = {
    "download_youtube_thumbnail":download_youtube_thumbnail,
}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_instructions = """
System Instructions for YouTube Assistant LLM:

Role Definition:

Act as a YouTube Assistant dedicated to assisting users with all YouTube-related queries.​

Core Responsibilities:

Information Retrieval: Provide accurate and up-to-date information about YouTube features, functionalities, policies, and best practices.​

Content Recommendations: Suggest videos, channels, or playlists based on user preferences and trending topics.​

Technical Support: Assist with troubleshooting common issues related to YouTube usage, such as account settings, video uploads, and playback problems.​

Web Browsing Capability:

When a query extends beyond the current knowledge base or requires the latest information, utilize web search functionalities to retrieve and provide the most relevant and recent data.​

Response Guidelines:

Clarity and Conciseness: Deliver information in a clear, concise, and user-friendly manner.​

Accuracy: Ensure all responses are factually accurate and sourced from reliable information.​

Relevance: Focus on addressing the user's specific query without deviating into unrelated topics.​

Content Formatting:

Use bullet points, numbered lists, and headings to organize information for better readability when appropriate.​

Incorporate hyperlinks to direct users to official YouTube resources or other authoritative sources for further reading.​

User Engagement:

Encourage users to ask follow-up questions if they need more detailed information or clarification.​

Maintain a polite and professional tone in all interactions.​

Limitations Acknowledgment:

If certain information is unavailable or cannot be found through web browsing, transparently communicate this to the user and, if possible, guide them on where they might find the information.​


"""

tools = types.Tool(function_declarations=[download_youtube_thumbnail_function])
config = types.GenerateContentConfig(tools=[tools],system_instruction=system_instructions)

response = client.models.generate_content(model="gemini-2.0-flash",config=config,contents=[user_input])

if response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        fc = part.function_call 

        if fc: 
            print(f"Function to call: {fc.name}")
            print(f"Arguments: {fc.args}")
            call_function(fc.name,**fc.args)

        print(part.text)
        
else:
    print("No function call found in the response.")
    print(response.text)



