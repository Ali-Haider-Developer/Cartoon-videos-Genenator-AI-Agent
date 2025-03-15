from typing import Dict, Any, List
import os
import cv2
import numpy as np
from PIL import Image
import io
import requests
import tempfile
from diffusers import StableVideoDiffusionPipeline, DiffusionPipeline
import torch

class VideoCreatorAgent:
    def __init__(self, api_key: str):
        self.huggingface_key = api_key
        self.frame_rate = 24
        self.resolution = (1920, 1080)
        self.temp_dir = tempfile.mkdtemp()
        self.mock_mode = True
        
        # Initialize the 3D animation pipelines
        if not self.mock_mode:
            # Initialize SVD pipeline for 2D to video
            self.svd_pipeline = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid-xt-1-1-tensorrt",
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True,
                token=self.huggingface_key
            ).to("cuda")

            # Initialize SV3D pipeline for 3D scene generation
            self.sv3d_pipeline = DiffusionPipeline.from_pretrained(
                "stabilityai/sv3d",
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True,
                token=self.huggingface_key
            ).to("cuda")

    async def generate_scene_frames(self, scene: Dict[str, Any], num_frames: int = 8) -> List[str]:
        """Generate animated frames using both SVD and SV3D"""
        try:
            if self.mock_mode:
                return await self.generate_mock_frames(scene, num_frames)

            # Create detailed prompt for the scene
            prompt = self._create_scene_prompt(scene)
            
            # First generate 3D scene using SV3D
            initial_frame = self.sv3d_pipeline(
                prompt=prompt,
                num_inference_steps=50,
                guidance_scale=7.5
            ).images[0]

            # Then generate video frames using SVD
            video_frames = self.svd_pipeline(
                image=initial_frame,
                num_frames=num_frames,
                num_inference_steps=50,
                min_guidance_scale=1.0,
                motion_bucket_id=127,
                noise_aug_strength=0.1
            ).frames[0]
            
            # Save frames
            frame_paths = []
            for i, frame in enumerate(video_frames):
                path = os.path.join(self.temp_dir, f"frame_{i}.png")
                frame.save(path)
                frame_paths.append(path)
                
            return frame_paths

        except Exception as e:
            print(f"Error generating frames: {str(e)}")
            return await self.generate_mock_frames(scene, num_frames)

    async def generate_mock_frames(self, scene: Dict[str, Any], num_frames: int = 8) -> List[str]:
        """Generate mock frames for testing"""
        frame_paths = []
        base_frame = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
        base_frame[:] = (50, 100, 150)

        # Add scene information
        y_position = 100
        for text in [
            f"Scene: {scene['description']}",
            f"Setting: {scene['setting']}",
            f"Characters: {', '.join(scene['characters_present'])}",
        ]:
            cv2.putText(base_frame, text, (100, y_position), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            y_position += 50

        # Save multiple slightly different frames
        for i in range(num_frames):
            frame = base_frame.copy()
            # Add frame number
            cv2.putText(frame, f"Frame {i+1}", (100, y_position), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            path = os.path.join(self.temp_dir, f"frame_{i}.png")
            cv2.imwrite(path, frame)
            frame_paths.append(path)

        return frame_paths

    def _create_scene_prompt(self, scene: Dict[str, Any]) -> str:
        """Create detailed prompt for 3D animation generation"""
        return f"""Create a cinematic 3D animated scene in Pixar/Disney style:
        Scene: {scene['description']}
        Setting: {scene['setting']}
        Characters: {', '.join(scene['characters_present'])}
        Action: {scene['action']}
        
        Style Requirements:
        - High-quality 3D animation
        - Expressive character animations
        - Dynamic lighting and shadows
        - Rich color palette
        - Cinematic composition
        
        Camera: {scene['animation_details']['camera_work']['movements'][0]}
        Angle: {scene['animation_details']['camera_work']['angles'][0]}
        
        Special Effects:
        - Magical: {', '.join(scene['animation_details']['special_effects']['magical'])}
        - Tech: {', '.join(scene['animation_details']['special_effects']['tech'])}
        
        Character Actions:
        {chr(10).join([f'- {char}: {action}' for char, action in scene['animation_details']['character_movements'].items()])}
        """

    async def download_image(self, url: str) -> str:
        """Download image from URL and save to temporary file"""
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img = img.resize(self.resolution)
            temp_path = os.path.join(self.temp_dir, f"frame_{hash(url)}.png")
            img.save(temp_path)
            return temp_path
        raise Exception(f"Failed to download image from {url}")

    async def create_scene(self, scene: Dict[str, Any], duration: float) -> str:
        """Create a scene using OpenCV"""
        frames = await self.generate_scene_frames(scene)
        frame_paths = [await self.download_image(frame) for frame in frames]
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_path = os.path.join(self.temp_dir, f"scene_{hash(str(scene))}.mp4")
        out = cv2.VideoWriter(temp_path, fourcc, self.frame_rate, self.resolution)
        
        for frame_path in frame_paths:
            frame = cv2.imread(frame_path)
            # Repeat frame to match duration
            for _ in range(int(duration * self.frame_rate / len(frame_paths))):
                out.write(frame)
        
        out.release()
        return temp_path

    async def generate_video(self, story: Dict[str, Any]) -> str:
        """Generate video from story"""
        try:
            if self.mock_mode:
                return await self.create_mock_video(story)

            # Original implementation
            total_duration = story["duration_minutes"] * 60
            scene_duration = total_duration / len(story["scene_breakdown"])
            
            scene_paths = []
            for scene in story["scene_breakdown"]:
                scene_path = await self.create_scene(scene, scene_duration)
                scene_paths.append(scene_path)
            
            output_path = os.path.join(self.temp_dir, f"{story['title']}.mp4")
            os.rename(scene_paths[0], output_path)
            return output_path
            
        except Exception as e:
            print(f"Error in generate_video: {str(e)}")
            # Fall back to mock video
            return await self.create_mock_video(story)

    async def create_mock_video(self, story: Dict[str, Any]) -> str:
        """Create a simple test video"""
        try:
            output_path = os.path.join(self.temp_dir, f"{story['title']}.mp4")
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, self.frame_rate, self.resolution)
            
            # Generate multiple scenes
            for scene in story['scene_breakdown']:
                # Create scene frame
                frame = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
                frame[:] = (50, 100, 150)
                
                # Add scene information
                y_position = 100
                for text in [
                    f"Episode {story.get('episode_number', 0)}: {story.get('title', 'Story')}",
                    f"Scene: {scene['description']}",
                    f"Setting: {scene['setting']}",
                    f"Characters: {', '.join(scene['characters_present'])}",
                ]:
                    cv2.putText(frame, text, (100, y_position), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    y_position += 50
                
                # Write scene frames (5 seconds per scene)
                for _ in range(5 * self.frame_rate):
                    out.write(frame)
            
            # Add ending credits
            credit_frame = np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
            credit_frame[:] = (30, 30, 30)
            cv2.putText(credit_frame, "Moral: " + story['moral_message'],
                       (100, self.resolution[1]//2), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 2)
            
            # Write credits (3 seconds)
            for _ in range(3 * self.frame_rate):
                out.write(credit_frame)
            
            out.release()
            return output_path
            
        except Exception as e:
            print(f"Error creating mock video: {str(e)}")
            raise Exception(f"Failed to create mock video: {str(e)}")
        finally:
            # Cleanup
            for file in os.listdir(self.temp_dir):
                if file.endswith(('.png', '.jpg', '.mp4')) and file != os.path.basename(output_path):
                    os.remove(os.path.join(self.temp_dir, file))
                    

