from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv
from agents.story_generator import StoryGeneratorAgent
from agents.sound_generator import SoundGeneratorAgent
from agents.video_creator import VideoCreatorAgent
from agents.memory_agent import MemoryAgent

load_dotenv()

app = FastAPI(title="Cartoon Video Editor Agent")

# Initialize agents
story_generator = StoryGeneratorAgent()
sound_generator = SoundGeneratorAgent()
video_creator = VideoCreatorAgent(api_key=os.getenv("HUGGINGFACE_API_KEY"))
memory_agent = MemoryAgent()

class StoryRequest(BaseModel):
    episode_number: int = Field(..., description="Episode number (1 for first episode, 2 for second, etc.)")
    theme: Optional[str] = None

@app.post("/generate-story")
async def generate_story(request: StoryRequest):
    try:
        # Generate story
        previous_stories = await memory_agent.get_previous_stories()
        new_story = await story_generator.generate_story(
            episode_number=request.episode_number,
            theme=request.theme,
            previous_stories=previous_stories
        )
        
        # Add story to memory
        story_id = await memory_agent.add_story(new_story)
        
        return {
            "id": story_id,
            "episode_number": request.episode_number,
            "story": new_story
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-sound/{story_id}")
async def generate_sound(story_id: int):
    try:
        # Get story
        story = await memory_agent.get_story(story_id)
        if not story:
            raise HTTPException(status_code=404, detail=f"Story with ID {story_id} not found")

        # Generate sound
        sound_path = await sound_generator.generate_sound(story)
        
        return FileResponse(
            sound_path,
            media_type="audio/mp3",
            filename=f"{story['title']}_audio.mp3"
        )

    except Exception as e:
        print(f"Error generating sound: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-video/{story_id}")
async def generate_video(story_id: int):
    try:
        # Get story
        story = await memory_agent.get_story(story_id)
        if not story:
            raise HTTPException(status_code=404, detail=f"Story with ID {story_id} not found")

        # Generate sound first
        sound_path = await sound_generator.generate_sound(story)
        
        # Generate video with sound
        video_path = await video_creator.generate_video(story, sound_path)
        
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"{story['title']}.mp4"
        )

    except Exception as e:
        print(f"Error generating video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 


