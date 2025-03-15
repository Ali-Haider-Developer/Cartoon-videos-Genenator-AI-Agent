from typing import Dict, Any, Optional
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from templates.prompt_template import STORY_PROMPT_TEMPLATE

class StoryGeneratorAgent:
    def __init__(self, api_key: str = None):
        # Load API key from .env if not provided
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = OpenAI(api_key=self.api_key)
        self.mock_mode = False  # Set to False to use real OpenAI API

    async def generate_story(self, episode_number: int, theme: Optional[str] = None, previous_stories: list = None) -> Dict[str, Any]:
        if self.mock_mode:
            return self.generate_mock_story(episode_number, theme)

        try:
            prompt = STORY_PROMPT_TEMPLATE.format(
                episode_number=episode_number,
                theme=theme if theme else "Continue the story from previous episodes",
                previous_stories=json.dumps(previous_stories if previous_stories else [], indent=2)
            )

            # Use GPT-4 for more creative and detailed stories
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # You can change this to "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": """You are a professional 3D animated series writer and director.
                    Generate detailed, engaging stories with cinematic scenes and precise animation instructions.
                    Focus on creating visually stunning moments that can be animated in 3D."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=4000,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )

            story = json.loads(response.choices[0].message.content)
            story["episode_number"] = episode_number
            return story

        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return self.generate_mock_story(episode_number, theme)

    def generate_mock_story(self, episode_number: int, theme: Optional[str] = None) -> Dict[str, Any]:
        return {
            "title": f"The Magic Portal Mystery - Episode {episode_number}",
            "episode_number": episode_number,
            "duration_minutes": 12,
            "main_character": {
                "name": "Leo the Brave",
                "type": "hero",
                "traits": ["curious", "adventurous", "fearless"],
                "background": "A young explorer who discovered the first magic portal",
                "catchphrase": "Adventure awaits!",
                "appearance": {
                    "style": "Modern 3D animated character",
                    "features": "Spiky brown hair, bright blue eyes, adventurer's outfit",
                    "colors": ["navy blue jacket", "tan pants", "golden explorer's badge"],
                    "animations": ["heroic pose", "determined smile", "acrobatic movements"]
                }
            },
            "supporting_characters": [
                {
                    "name": "Mia the Genius",
                    "type": "inventor",
                    "role": "Tech expert and gadget creator",
                    "special_ability": "Creates amazing scientific gadgets",
                    "appearance": {
                        "style": "Smart and quirky",
                        "features": "Purple hair with science goggles, lab coat with glowing circuits",
                        "colors": ["white lab coat", "purple hair", "glowing blue accents"],
                        "animations": ["excited gestures", "adjusting goggles", "typing holographic displays"]
                    }
                },
                {
                    "name": "Ziggy",
                    "type": "talking_animal",
                    "role": "Comic relief and memory keeper",
                    "special_ability": "Perfect memory for important clues",
                    "appearance": {
                        "style": "Cute and fluffy",
                        "features": "Spiky brown hair, bright blue eyes, squirrel-like ears",
                        "colors": ["tan fur", "golden belt", "navy blue jacket"],
                        "animations": ["playful grin", "curious tilt", "running squirrel"]
                    }
                },
                {
                    "name": "Professor Wizzle",
                    "type": "mentor",
                    "role": "Wise but forgetful guide",
                    "special_ability": "Ancient magical knowledge",
                    "appearance": {
                        "style": "Old and wise",
                        "features": "White beard, wizard hat, long robes",
                        "colors": ["gray robes", "wizard hat", "golden accessories"],
                        "animations": ["reading upside down", "levitating", "casting magical spells"]
                    }
                }
            ],
            "story_connectors": {
                "magical_elements": ["mystical portal", "enchanted compass", "time-bending hourglass"],
                "special_gadgets": ["portal detector", "anti-gravity boots", "holographic map"]
            },
            "plot_summary": f"In Episode {episode_number}, Leo and his friends discover a mysterious new portal leading to a world of floating islands. When King Gloom attempts to steal the portal's power, the team must use Mia's latest invention and Ziggy's perfect memory to solve an ancient puzzle. Professor Wizzle provides cryptic but crucial advice, while RoboMax protects the team from Bloop and Blip's chaotic interference.",
            "visual_style": {
                "character_design": "Modern 3D animation with expressive features",
                "animation_style": "Fluid and dynamic like modern Pixar films",
                "color_palette": ["magical purple", "adventurous orange", "mystical blue"],
                "lighting_mood": "Dynamic lighting with magical particle effects"
            },
            "scene_breakdown": [
                {
                    "description": "Opening scene in Professor Wizzle's library",
                    "setting": "Magical library with floating books and glowing portals",
                    "characters_present": ["Leo", "Mia", "Ziggy", "Professor Wizzle"],
                    "action": "Team discovers ancient map revealing new portal location",
                    "animation_details": {
                        "character_movements": {
                            "Leo": "Climbs floating book stacks athletically",
                            "Mia": "Uses holographic scanner on ancient texts",
                            "Ziggy": "Bounces between floating books",
                            "Professor Wizzle": "Levitates while reading upside down"
                        },
                        "camera_work": {
                            "movements": ["sweeping crane shot", "character close-ups", "dynamic tracking"],
                            "angles": ["low angle hero shots", "overhead library view", "dutch angles for tension"]
                        },
                        "special_effects": {
                            "magical": ["sparkling book trails", "glowing portal energies", "floating dust particles"],
                            "tech": ["holographic displays", "scanning beams", "gadget interfaces"]
                        }
                    },
                    "comedy_moments": [
                        {"moment": "Ziggy gets caught in floating book tornado", "animation": "Spinning squirrel with flying books"},
                        {"moment": "Professor Wizzle reads book upside down", "animation": "Glasses slowly sliding up forehead"}
                    ],
                    "duration_seconds": 180  # 3 minutes for opening scene
                },
                {
                    "description": "Portal discovery scene",
                    "setting": "Mysterious cave with crystal formations",
                    "characters_present": ["Leo", "Mia", "RoboMax", "King Gloom"],
                    "action": "Team activates portal while avoiding King Gloom",
                    "comedy_moments": [
                        "King Gloom trips on his cape",
                        "Bloop and Blip phase through wrong walls"
                    ],
                    "camera_movements": "Action-packed tracking shots",
                    "lighting_setup": "Dynamic crystal reflections",
                    "special_effects": ["portal energy", "crystal gleams", "magical beams"]
                }
            ],
            "moral_message": "Teamwork and creativity can overcome any obstacle",
            "musical_moments": [
                "Magical discovery theme",
                "Action sequence symphony",
                "Victory celebration song"
            ],
            "next_episode_hook": "As the team celebrates their victory, Flora the Fairy appears with urgent news about a disturbance in the portal network..."
        }
    