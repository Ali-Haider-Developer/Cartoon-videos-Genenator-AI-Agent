from typing import List, Dict, Any
import json
import os

class MemoryAgent:
    def __init__(self):
        self.stories_history = {}
        self.current_id = 0
        self.storage_path = "storage/stories.json"
        self._load_stories()
        
        # Create storage directory if it doesn't exist
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _load_stories(self):
        """Load stories from storage if exists"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                try:
                    data = json.load(f)
                    # Handle old format (list of stories)
                    if isinstance(data, list):
                        self.stories_history = {}
                        for i, story in enumerate(data, 1):
                            story['id'] = i
                            self.stories_history[str(i)] = story
                        self.current_id = len(data)
                    # Handle new format (dict with stories and current_id)
                    else:
                        self.stories_history = data.get('stories', {})
                        self.current_id = data.get('current_id', 0)
                except Exception as e:
                    print(f"Error loading stories: {e}")
                    self.stories_history = {}
                    self.current_id = 0

    def _save_stories(self):
        """Save stories to storage"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump({
                'stories': self.stories_history,
                'current_id': self.current_id
            }, f, indent=2)

    async def add_story(self, story: Dict[str, Any]) -> int:
        """Add story to history and return its ID"""
        self.current_id += 1
        story['id'] = self.current_id
        self.stories_history[str(self.current_id)] = story
        self._save_stories()
        return self.current_id

    async def get_previous_stories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get previous stories up to limit"""
        stories = list(self.stories_history.values())
        return stories[-limit:] if stories else []

    async def get_story(self, story_id: int) -> Dict[str, Any]:
        """Get story by ID"""
        return self.stories_history.get(str(story_id))

    async def check_similarity(self, new_story: Dict[str, Any]) -> bool:
        if not self.stories_history:
            return False
            
        # Simple title and plot comparison
        for story in self.stories_history.values():
            if (story['title'].lower() == new_story['title'].lower() or 
                story['plot_summary'].lower() == new_story['plot_summary'].lower()):
                return True
        return False 