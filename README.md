# SubStream

## TODO

- [ ] Phase 1: Environment & System Setup

  - [x] Initialize Project: Create a new directory, set up a Python virtual environment (venv), and initialize Git.

  - [x] Install Python Libraries: Install fastapi, uvicorn, python-multipart (for uploads), moviepy, openai-whisper, scenedetect, and indic-transliteration.

  - [x] Install ImageMagick: Download and install ImageMagick (required by MoviePy for text).

    - [ ] Configuration: Edit moviepy config file to point to the ImageMagick binary if not detected automatically.

  - [x] Install FFmpeg: Ensure FFmpeg is installed and added to your system PATH.

  - [x] Acquire Fonts:

    - [x] Download a Devanagari-supported .ttf font (e.g., Google Noto Sans Devanagari or Mangal) for Hindi text.

    - [x] Verify a standard English font (e.g., Arial) is available.

- [ ] Phase 2: The API Skeleton (FastAPI)

  - [x] Create Main App: Set up main.py with a basic FastAPI instance.

  - [ ] Temp Directory Logic: Create a utility function to manage temp/ folders for uploads and processed outputs.

  - [ ] Endpoint 1 (Upload): Create POST /process-video that:

    - [ ] Accepts a video file (UploadFile).

    - [ ] Accepts a form field for language_mode ("english", "hindi", "hinglish").

    - [ ] Saves the video locally.

    - [ ] Triggers a Background Task.

    - [ ] Returns a job_id immediately.

  - [ ] Endpoint 2 (Status): Create GET /status/{job_id} to check if processing is done.

  - [ ] Endpoint 3 (Download): Create GET /download/{job_id} to serve the final .mp4 using FileResponse.

- [ ] Phase 3: Core Logic - Audio & Transcription

  - [ ] Audio Extraction: Write a function using moviepy to strip audio from the input video to a temp .mp3 or .wav file.

  - [ ] Whisper Integration:

    - [ ] Write a function to load the Whisper model (start with base model).

    - [ ] Logic Branch A (English): If user selects English, run model.transcribe(audio, language='en').

    - [ ] Logic Branch B (Hindi/Hinglish): If user selects Hindi/Hinglish, run model.transcribe(audio, language='hi').

  - [ ] Transliteration Engine (The Hinglish Logic):

    - [ ] Create a helper function using indic-transliteration.

    - [ ] Input: Devanagari text string (from Whisper).

    - [ ] Output: Romanized text string (Hinglish).

    - [ ] Integrate this into the pipeline only if language_mode == "hinglish".

- [ ] Phase 4: Video Processing (The "Burn-in")

  - [ ] Subtitle Segment Processor:

    - [ ] Create a function that iterates through Whisper segments.

    - [ ] Font Selector: Logic to choose the .ttf path based on language (Hindi Font vs English Font).

  - [ ] Clip Generation:

    - [ ] Generate a TextClip (MoviePy) for each subtitle segment.

    - [ ] Configure styling: Font size (relative to video height), Color (White), Stroke (Black border), Position (Bottom Center).

    - [ ] Set the start_time and duration for each TextClip based on Whisper timestamps.

  - [ ] Compositing:

    - [ ] Load original video as VideoFileClip.

    - [ ] Create a CompositeVideoClip combining the Original Video + List of TextClips.

  - [ ] Rendering:

    - [ ] Write the final video using write_videofile.

    - [ ] Settings: codec='libx264', audio_codec='aac', threads=4 (or more).

- [ ] Phase 5: Cleanup & Optimization

  - [ ] Garbage Collection: Write a utility to delete the uploaded raw video and the extracted audio file after processing is complete (keep only the final output).

  - [ ] Error Handling: Add try/except blocks to catch Whisper failures or MoviePy rendering errors and update the job status to "failed".

  - [ ] GPU Check: Add a startup check to see if CUDA is available for Whisper (prints a warning if running on CPU).
