import pygame
import random
import os

class MusicManager:
    def __init__(self):
        # Define the playlist
        self.music_tracks = ["clarity.ogg", "soft_spot.ogg", "con_gai_mien_tay.ogg", "wantchu.ogg", "war.ogg"]
        self.current_track_index = 0

        # Shuffle so it plays at random each launch
        random.shuffle(self.music_tracks)

    def start_music(self):
        """Call this once at game startup"""
        self._play_current_track()

    def update(self):
        """Call this every frame in the game loop"""
        if not pygame.mixer.music.get_busy():
            self.play_next_song()

    def play_next_song(self):
        """Switches to the next song in the shuffled queue"""
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        self._play_current_track()

    def _play_current_track(self):
        """Internal method to actually load and play the file"""
        try:
            track_name = self.music_tracks[self.current_track_index]
            track_path = os.path.join("resources", "audio", track_name)

            print(f"MusicManager: Now playing {track_name}")
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"MusicManager Error: Could not play {track_path}: {e}")

