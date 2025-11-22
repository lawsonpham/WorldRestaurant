import pygame
import random
import os

class MusicManager:
    def __init__(self):
        # --- MUSIC SETUP ---
        self.music_tracks = ["clarity.ogg", "soft_spot.ogg", "con_gai_mien_tay.ogg", "wantchu.ogg", "war.ogg"]
        self.current_track_index = 0
        random.shuffle(self.music_tracks)

        # --- SFX SETUP (Pre-load sounds here) ---
        self.sfx = {}
        self._load_sfx("pop")

    def _load_sfx(self, name):
        """Helper to load a sound file into memory once"""
        try:
            path = os.path.join("resources", "audio", "sfx", f"{name}.ogg")
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.5)
            self.sfx[name] = sound
            print(f"MusicManager: Loaded SFX {name}")
        except Exception as e:
            print(f"MusicManager Error: Could not load SFX {path}: {e}")

    def start_music(self):
        self._play_current_track()

    def update(self):
        if not pygame.mixer.music.get_busy():
            self.play_next_song()

    def play_next_song(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        self._play_current_track()

    def _play_current_track(self):
        try:
            track_name = self.music_tracks[self.current_track_index]
            track_path = os.path.join("resources", "audio", track_name)
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
            print(f"MusicManager: Now playing {track_name}")
        except Exception as e:
            print(f"MusicManager Error: Could not play {track_path}: {e}")

    def play_sfx(self, sfx_name):
        """Plays a pre-loaded sound effect"""
        if sfx_name in self.sfx:
            self.sfx[sfx_name].play()
        else:
            print(f"MusicManager Warning: SFX '{sfx_name}' not loaded!")
