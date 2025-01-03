# Pomodoro Timer

A simple Pomodoro Timer application built with Python and Streamlit, following SOLID principles.

## Features

- Preset timer durations (5, 15, 30, 45 minutes)
- Custom duration option
- Play, pause, and reset functionality
- Visual and audio alerts when timer completes
- Clean, intuitive interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jaimeman84/pomodoro-timer.git
cd pomodoro-timer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
streamlit run src/app.py
```

## Requirements

Create a `requirements.txt` file with:
```
streamlit>=1.10.0
pytest>=7.0.0
```

## Project Structure

- `src/timer.py`: Core timer logic
- `src/sound_manager.py`: Sound effect management
- `src/app.py`: Streamlit application
- `tests/`: Unit tests

## Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request