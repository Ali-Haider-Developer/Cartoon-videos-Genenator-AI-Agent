STORY_PROMPT_TEMPLATE = """
Create a detailed 3D animated cartoon story for Episode {episode_number}.

Theme: {theme}

Previous episodes context:
{previous_stories}

🌟 Main Characters 🌟
1. Leo the Brave 🦸‍♂️
   * Role: Main protagonist and leader
   * Traits: Curious, adventurous, fearless
   * Special ability: Natural leadership and courage
   * Catchphrase: "Adventure awaits!"

2. Mia the Genius 🧠
   * Role: Tech expert and inventor
   * Traits: Intelligent, resourceful, creative
   * Special ability: Creates amazing gadgets
   * Catchphrase: "There's a scientific solution!"

3. Ziggy the Talking Squirrel 🐿️
   * Role: Comic relief and memory bank
   * Traits: Mischievous, clever, witty
   * Special ability: Perfect memory for clues
   * Catchphrase: "Nuts! I remember something!"

4. Professor Wizzle 🧙‍♂️
   * Role: Mentor and guide
   * Traits: Wise, eccentric, forgetful
   * Special ability: Magical knowledge
   * Catchphrase: "By the books of wisdom!"

5. RoboMax 🤖
   * Role: Team protector
   * Traits: Strong, loyal, literal-minded
   * Special ability: Super strength and shields
   * Catchphrase: "Protection mode activated!"

Villains:
1. King Gloom 😈
   * Role: Main antagonist
   * Traits: Power-hungry but clumsy
   * Goal: Steal the magic portal's power
   * Catchphrase: "The power will be mine... oops!"

2. Bloop & Blip 👻👻
   * Role: Minion ghosts
   * Traits: Goofy, incompetent, lovable
   * Special ability: Can phase through walls (usually into wrong rooms)
   * Catchphrase: "Double trouble... or not!"

Helper:
Flora the Fairy 🧚
   * Role: Magical assistant
   * Traits: Kind, helpful, mysterious
   * Special ability: Provides magical hints and aid
   * Catchphrase: "A sprinkle of magic helps!"

Story Requirements:
1. Each episode should:
   * Feature at least 4 main characters
   * Include one magical challenge or mystery
   * Have a moral lesson
   * Contain humor and heart
   * End with a small cliffhanger or setup for next episode

2. Story Elements:
   * Magical portals or doorways
   * Creative gadgets from Mia
   * Comedic moments with Ziggy/Bloop & Blip
   * Wise (but sometimes confusing) advice from Professor Wizzle
   * Action scenes with RoboMax
   * King Gloom's failed schemes

Please provide the story in the following JSON format:
{{
    "title": "Story title",
    "duration_minutes": "integer between 10-15",
    "main_character": {{
        "name": "character name",
        "type": "hero/sidekick/talking_animal/etc",
        "traits": ["trait1", "trait2"],
        "background": "character background",
        "catchphrase": "memorable catchphrase"
    }},
    "supporting_characters": [
        {{
            "name": "character name",
            "type": "character type",
            "role": "role description",
            "special_ability": "unique ability"
        }}
    ],
    "story_connectors": {{
        "magical_elements": ["element1", "element2"],
        "special_gadgets": ["gadget1", "gadget2"]
    }},
    "plot_summary": "detailed plot summary",
    "visual_style": {{
        "character_design": "3D modeling details",
        "animation_style": "animation reference and style",
        "color_palette": ["color1", "color2", "color3"],
        "lighting_mood": "lighting style description"
    }},
    "scene_breakdown": [
        {{
            "description": "scene description",
            "setting": "scene location",
            "characters_present": ["character1", "character2"],
            "action": "what happens in the scene",
            "comedy_moments": ["moment1", "moment2"],
            "camera_movements": "camera directions",
            "lighting_setup": "lighting description",
            "special_effects": ["effect1", "effect2"]
        }}
    ],
    "moral_message": "lesson or moral of the story",
    "musical_moments": ["moment1", "moment2"],
    "next_episode_hook": "setup for the next episode"
}}
""" 