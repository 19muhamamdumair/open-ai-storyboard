import openai
import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    OPENAI_API_KEY = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


app = FastAPI()

class ScriptPayload(BaseModel):
    objective:str
    age:str
    gender:str
    income:str
    occupation:str
    education:str
    location:str
    theme:str

class StoryBoardPayload(BaseModel):
    previous_prompt:str
    

@app.post("/generate-advertising-script")
async def index(payload:ScriptPayload=None):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt_advertiser(payload),
        temperature=0.5,
        max_tokens=4000-len(generate_prompt_advertiser(payload)),
    )
    result = response.choices[0].text.replace("\n", "\n")
    return result

@app.post("/generate-screenwriting-script")
async def index(payload:StoryBoardPayload):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt_screenwriter(payload),
        temperature=0.5,
        max_tokens=4000-len(generate_prompt_screenwriter(payload)),
    )
    result = response.choices[0].text.replace("\n", "\n")
    return result

@app.post("/generate-prompt")
async def index(payload:StoryBoardPayload):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt_dalle(payload),
        temperature=0.5,
        max_tokens=4000-len(generate_prompt_dalle(payload)),
    )
    result = response.choices[0].text.replace("\n", "\n")
    # new_string = result.replace("\n", "\n")

    return result


def generate_prompt_advertiser(payload):
    input="""
    I want you to act as an advertiser.
  You will create a campaign to promote a product or service from given details.
  Your strong side is developing a condensed key message.
  I need your help creating a clear packaged message for a campaign from below parameters.
  I want you to only reply with one compelling ad.
  Do not write any explanations unless I instruct you to do so.

  Objective:{}
  Target Audience:
  - Age:{} 
  - Gender: {} 
  - Income: {}
  - Occupation: {}
  - Education: {}
  - Location:{}
  Main Message/Theme:  {}

  Script:""".format(
        payload.objective,
        payload.age,
        payload.gender,
        payload.income,
        payload.occupation,
        payload.education,
        payload.location,
        payload.theme
  )
    return input



def generate_prompt_screenwriter(payload):
    input="""I want you to act as a screenwriter.
    Your previous result as an advertiser to create a campaign to promote a product or service is {}
    You will come up an engaging and creative storyboards for digital ad videos that can captivate its viewers.
    Stories must be imaginative and captivating. It can be fairy tales, educational stories or any other type of stories which has the potential to capture people's attention and imagination. Depending on the target audience, you may choose specific themes or topics for your storyboard e.g., if it's children then you can talk about animals;
    If it's adults then history-based tales might engage them better etc.
    My first request is taking above information develop a storyboard for 30 second digital ad video animation with minimum 8 scenes with end screen which includes brand tagline. 
    The story-board format is a scene-by-scene description. Besides text describing scene,
    also add voiceover text where necessary. Make it friendly.
    Do not write any explanations unless I instruct you to do so.""".format(payload.previous_prompt)
    
    return input



def generate_prompt_dalle(payload):
    input="""Now I want you to act as a prompt generator for DALL-E's artificial intelligence program.
    Your previous result as a screenwriter is:  {}
    Your job is to provide detailed and creative descriptions that will inspire unique and interesting images from the AI.
    Keep in mind that the AI is capable of understanding a wide range of language and can interpret abstract concepts,
    so feel free to be as imaginative and descriptive as possible. 
    For example, you could describe a scene from a futuristic city, or a surreal landscape filled with strange creatures.
    The more detailed and imaginative your description, the more interesting the resulting image will be.
    My first request is taking each scene from above, convert each into prompt accordingly, 
    but make sure to keep the output as close to the scene as possible. 
    Do not add or remove anything that would change the story. 
    Make sure each prompt begins with modern flat style illustration""".format(payload.previous_prompt)
    
    return input


if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)