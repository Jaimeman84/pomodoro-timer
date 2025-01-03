import streamlit as st
import time
from sound_manager import SoundPlayer
import platform

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'duration' not in st.session_state:
        st.session_state.duration = 300  # 5 minutes default
    if 'remaining_time' not in st.session_state:
        st.session_state.remaining_time = st.session_state.duration
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'flash' not in st.session_state:
        st.session_state.flash = False
    if 'sound_player' not in st.session_state:
        st.session_state.sound_player = SoundPlayer()
    if 'timer_complete' not in st.session_state:
        st.session_state.timer_complete = False

def format_time(seconds):
    """Format seconds into MM:SS string"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def update_timer():
    """Update timer if running"""
    if st.session_state.is_running:
        if st.session_state.last_update is None:
            st.session_state.last_update = time.time()
        
        current_time = time.time()
        elapsed = current_time - st.session_state.last_update
        st.session_state.remaining_time -= elapsed
        st.session_state.last_update = current_time
        
        if st.session_state.remaining_time <= 0:
            st.session_state.remaining_time = 0
            st.session_state.is_running = False
            st.session_state.flash = True
            st.session_state.timer_complete = True
            # Play sound when timer completes
            st.session_state.sound_player.play_in_thread(10)  # Play for 10 seconds
            st.balloons()

def main():
    st.set_page_config(
        page_title="Pomodoro Timer",
        page_icon="🍅",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # App title and description
    st.title("🍅 Pomodoro Timer")
    st.write("Stay focused and productive with the Pomodoro Technique!")
    
    # Timer duration selection
    duration_options = {
        "5 minutes": 300,
        "15 minutes": 900,
        "30 minutes": 1800,
        "45 minutes": 2700,
        "Custom": 0
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_duration = st.selectbox(
            "Select Duration",
            options=list(duration_options.keys()),
            key="duration_select"
        )
    
    # Handle custom duration
    with col2:
        if selected_duration == "Custom":
            custom_minutes = st.number_input(
                "Minutes",
                min_value=1,
                max_value=120,
                value=25
            )
            new_duration = custom_minutes * 60
        else:
            new_duration = duration_options[selected_duration]
    
    # Update duration if changed and timer is not running
    if not st.session_state.is_running and new_duration != st.session_state.duration:
        st.session_state.duration = new_duration
        st.session_state.remaining_time = new_duration
        st.session_state.timer_complete = False
    
    # Display timer
    st.markdown(
        f"<h1 style='text-align: center; font-size: 4em;'>{format_time(max(0, st.session_state.remaining_time))}</h1>",
        unsafe_allow_html=True
    )
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        start_stop = st.button(
            "⏸️ Pause" if st.session_state.is_running else "▶️ Start",
            use_container_width=True
        )
        if start_stop:
            if st.session_state.is_running:
                st.session_state.is_running = False
                st.session_state.last_update = None
            else:
                if st.session_state.remaining_time > 0:
                    st.session_state.is_running = True
                    st.session_state.last_update = time.time()
                    st.session_state.timer_complete = False
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.is_running = False
            st.session_state.remaining_time = st.session_state.duration
            st.session_state.last_update = None
            st.session_state.flash = False
            st.session_state.timer_complete = False
            st.session_state.sound_player.stop_beep()
    
    with col3:
        status = "Running" if st.session_state.is_running else "Paused"
        st.markdown(f"<div style='text-align: center; padding: 15px;'>Status: {status}</div>", unsafe_allow_html=True)
    
    # Update timer if running
    if st.session_state.is_running:
        update_timer()
        time.sleep(0.1)  # Small delay to prevent too frequent updates
        st.rerun()
    
    # Flash effect when timer completes
    if st.session_state.flash:
        st.markdown(
            """
            <style>
                .stApp {
                    animation: flash 1s infinite;
                }
                @keyframes flash {
                    0% { background-color: white; }
                    50% { background-color: #ff4b4b; }
                    100% { background-color: white; }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    # Show completion message
    if st.session_state.timer_complete:
        st.success("Time's up! Take a break! 🎉")
    
    # Add footer with instructions
    st.markdown("---")
    st.markdown("""
    **Instructions:**
    1. Select a preset duration or enter a custom time
    2. Click Start to begin the timer
    3. Use Pause to temporarily stop the timer
    4. Use Reset to start over
    """)
    
    # Add credits
    st.markdown("---")
    st.markdown("Made with ❤️ by Jaime Mantilla, MSIT + AI")

if __name__ == "__main__":
    main()