import time
from typing import Optional, Callable

class Timer:
    """Timer class implementing core timer functionality"""
    
    def __init__(self, on_complete: Optional[Callable] = None):
        """Initialize timer"""
        self.duration: int = 0
        self.remaining_time: int = 0
        self.is_running: bool = False
        self.last_update: Optional[float] = None
        self.on_complete = on_complete
    
    def set_duration(self, duration_seconds: int) -> None:
        """Set timer duration and reset remaining time"""
        self.duration = duration_seconds
        self.remaining_time = duration_seconds
        self.is_running = False
        self.last_update = None
    
    def start(self) -> None:
        """Start or resume the timer"""
        if self.remaining_time > 0:
            self.is_running = True
            self.last_update = time.time()
    
    def pause(self) -> None:
        """Pause the timer"""
        if self.is_running:
            self.update()  # Update time before pausing
        self.is_running = False
        self.last_update = None
    
    def reset(self) -> None:
        """Reset timer to initial duration"""
        self.remaining_time = self.duration
        self.is_running = False
        self.last_update = None
    
    def update(self) -> None:
        """Update timer state and check for completion"""
        if not self.is_running or self.last_update is None:
            return
        
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        
        self.remaining_time = max(0, self.remaining_time - int(elapsed))
        
        if self.remaining_time == 0:
            self.is_running = False
            self.last_update = None
            if self.on_complete:
                self.on_complete()