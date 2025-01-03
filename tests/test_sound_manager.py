import pytest
import threading
import time
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sound_manager import SoundPlayer

class TestSoundPlayer:
    """Test suite for SoundPlayer class"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.sound_player = SoundPlayer()
    
    def teardown_method(self):
        """Cleanup method run after each test"""
        if self.sound_player.is_playing:
            self.sound_player.stop_beep()
    
    def test_initialization(self):
        """Test SoundPlayer initialization"""
        assert not self.sound_player.is_playing
        assert isinstance(self.sound_player.stop_flag, threading.Event)
        assert not self.sound_player.stop_flag.is_set()
    
    @patch('winsound.Beep')
    def test_play_stop_beep_windows(self, mock_beep):
        """Test playing and stopping beep on Windows"""
        with patch.object(self.sound_player, 'system', 'Windows'):
            # Start playing in thread
            self.sound_player.play_in_thread(duration=1)
            
            # Check if playing started
            time.sleep(0.1)
            assert self.sound_player.is_playing
            
            # Stop playing
            self.sound_player.stop_beep()
            time.sleep(0.1)
            
            # Verify stopped
            assert not self.sound_player.is_playing
            assert self.sound_player.stop_flag.is_set()
    
    @patch('os.system')
    def test_play_stop_beep_unix(self, mock_system):
        """Test playing and stopping beep on Unix"""
        with patch.object(self.sound_player, 'system', 'Linux'):
            # Start playing in thread
            self.sound_player.play_in_thread(duration=1)
            
            # Check if playing started
            time.sleep(0.1)
            assert self.sound_player.is_playing
            
            # Stop playing
            self.sound_player.stop_beep()
            time.sleep(0.1)
            
            # Verify stopped
            assert not self.sound_player.is_playing
            assert self.sound_player.stop_flag.is_set()
    
    @patch('winsound.Beep')
    def test_auto_stop_after_duration(self, mock_beep):
        """Test that beep stops automatically after duration"""
        with patch.object(self.sound_player, 'system', 'Windows'):
            # Start playing with short duration
            self.sound_player.play_in_thread(duration=0.5)
            
            # Check if playing started
            time.sleep(0.1)
            assert self.sound_player.is_playing
            
            # Wait for duration plus small buffer
            time.sleep(0.7)
            
            # Verify stopped automatically
            assert not self.sound_player.is_playing
    
    @patch('winsound.Beep')
    def test_multiple_play_calls(self, mock_beep):
        """Test handling multiple play calls"""
        with patch.object(self.sound_player, 'system', 'Windows'):
            # Start first play
            self.sound_player.play_in_thread(duration=1)
            time.sleep(0.1)
            assert self.sound_player.is_playing
            
            # Start second play while first is running
            self.sound_player.play_in_thread(duration=1)
            time.sleep(0.1)
            
            # Verify still playing
            assert self.sound_player.is_playing
            
            # Stop playing
            self.sound_player.stop_beep()
            time.sleep(0.1)
            assert not self.sound_player.is_playing
    
    def test_stop_when_not_playing(self):
        """Test stopping when no sound is playing"""
        assert not self.sound_player.is_playing
        self.sound_player.stop_beep()  # Should not raise any errors
        assert not self.sound_player.is_playing
    
    @patch('threading.Thread')
    def test_thread_daemon_status(self, mock_thread):
        """Test that sound playing thread is created as daemon"""
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        
        self.sound_player.play_in_thread(duration=1)
        
        mock_thread.assert_called_once()
        assert mock_thread_instance.daemon
        mock_thread_instance.start.assert_called_once()

if __name__ == '__main__':
    pytest.main([__file__])