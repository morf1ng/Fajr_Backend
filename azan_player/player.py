import pygame
import os
from typing import Dict
from fastapi import HTTPException

class AzanPlayer:
    def __init__(self, sounds_dir: str = "azan_sounds"):
        pygame.mixer.init()
        self.sounds_dir = sounds_dir
        self.sound_files = {
            1: "azan1.mp3",
            2: "azan2.mp3",
            3: "azan3.mp3",
            4: "azan4.mp3",
            5: "azan5.mp3"
        }
        self._verify_files()

    def _verify_files(self):
        
        for num, filename in self.sound_files.items():
            path = os.path.join(self.sounds_dir, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Sound file for azan {num} not found: {filename}")

    def play_azan(self, azan_number: int, volume: float = 1.0):
        
        if azan_number not in self.sound_files:
            raise HTTPException(status_code=400, detail="Invalid azan number. Choose between 1-5")
        
        sound_file = self.sound_files[azan_number]
        sound_path = os.path.join(self.sounds_dir, sound_file)
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    def stop(self):
        
        pygame.mixer.music.stop()

    def get_status(self) -> Dict:
        
        return {
            "is_playing": pygame.mixer.music.get_busy(),
            "position": pygame.mixer.music.get_pos() if pygame.mixer.music.get_busy() else 0
        }