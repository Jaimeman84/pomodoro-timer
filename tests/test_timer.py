import pytest
import time
from unittest.mock import patch
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.timer import Timer

class TestTimer:
    """Test suite for Timer class"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.timer = Timer()
        self.duration = 300  # 5 minutes
    
    def test_initialization(self):
        """Test timer initialization"""
        assert self.timer.remaining_time == 0
        assert not self.timer.is_running
        assert self.timer.last_update is None
    
    def test_set_duration(self):
        """Test setting timer duration"""
        self.timer.set_duration(self.duration)
        assert self.timer.duration == self.duration
        assert self.timer.remaining_time == self.duration
        assert not self.timer.is_running
    
    def test_start_stop(self):
        """Test starting and stopping timer"""
        self.timer.set_duration(self.duration)
        
        # Test start
        self.timer.start()
        assert self.timer.is_running
        assert self.timer.last_update is not None
        
        # Test pause
        self.timer.pause()
        assert not self.timer.is_running
        assert self.timer.last_update is None
    
    def test_reset(self):
        """Test resetting timer"""
        self.timer.set_duration(self.duration)
        self.timer.start()
        time.sleep(0.1)  # Let some time pass
        self.timer.reset()
        
        assert self.timer.remaining_time == self.duration
        assert not self.timer.is_running
        assert self.timer.last_update is None
    
    @patch('time.time')
    def test_update_time_calculation(self, mock_time):
        """Test time calculation in update method"""
        self.timer.set_duration(60)  # 1 minute
        
        # Mock time progression
        mock_time.side_effect = [0, 10]  # 10 seconds elapsed
        
        self.timer.start()
        self.timer.update()
        
        assert self.timer.remaining_time == 50  # 60 - 10 seconds
    
    def test_timer_completion(self):
        """Test timer completion"""
        completion_called = False
        
        def on_complete():
            nonlocal completion_called
            completion_called = True
        
        timer = Timer(on_complete=on_complete)
        timer.set_duration(1)  # 1 second
        timer.start()
        
        # Force timer completion
        timer.remaining_time = 0
        timer.update()
        
        assert completion_called
        assert not timer.is_running
    
    def test_update_when_not_running(self):
        """Test update when timer is not running"""
        self.timer.set_duration(self.duration)
        initial_time = self.timer.remaining_time
        self.timer.update()
        
        assert self.timer.remaining_time == initial_time
    
    def test_start_with_zero_remaining(self):
        """Test starting timer with zero time remaining"""
        self.timer.set_duration(0)
        self.timer.start()
        
        assert not self.timer.is_running
        assert self.timer.remaining_time == 0
    
    def test_pause_resume(self):
        """Test pausing and resuming timer"""
        self.timer.set_duration(self.duration)
        
        # Start timer
        self.timer.start()
        time.sleep(0.1)
        
        # Pause timer
        self.timer.pause()
        remaining_at_pause = self.timer.remaining_time
        
        # Wait some time
        time.sleep(0.1)
        
        # Verify time didn't change while paused
        assert self.timer.remaining_time == remaining_at_pause
        
        # Resume timer
        self.timer.start()
        assert self.timer.is_running

if __name__ == '__main__':
    pytest.main([__file__])