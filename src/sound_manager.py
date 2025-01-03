import platform
import threading
import time

class SoundPlayer:
    def __init__(self):
        self.system = platform.system()
        self.is_playing = False
        self.stop_flag = threading.Event()

    def play_beep(self, duration=10):
        """Play beep sound based on operating system"""
        self.stop_flag.clear()
        self.is_playing = True
        
        if self.system == "Windows":
            self._play_windows_beep(duration)
        else:
            self._play_unix_beep(duration)

    def stop_beep(self):
        """Stop the beeping sound"""
        self.stop_flag.set()
        self.is_playing = False

    def _play_windows_beep(self, duration):
        """Play beep sound on Windows"""
        import winsound
        start_time = time.time()
        
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            winsound.Beep(1000, 500)  # 1000Hz for 500ms
            time.sleep(0.5)  # Wait 500ms between beeps
        
        self.is_playing = False

    def _play_unix_beep(self, duration):
        """Play beep sound on Unix-like systems"""
        import os
        start_time = time.time()
        
        while time.time() - start_time < duration and not self.stop_flag.is_set():
            os.system('play -nq -t alsa synth 0.5 sine 1000 2>/dev/null || beep')
            time.sleep(0.5)
        
        self.is_playing = False

    def play_in_thread(self, duration=10):
        """Play sound in a separate thread"""
        thread = threading.Thread(target=self.play_beep, args=(duration,))
        thread.daemon = True
        thread.start()