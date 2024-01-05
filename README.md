# animalGPT_behind_the_scenes
Working directory of animalGPT

Speaker Identification process for training
- [x] Common steps
   - [x] Extract audio file from video, convert to WAV format. Expected output: `audio.wav`
1. Speaker identification on complete file. Expected output
   ```py
   speaker_with_timestamps=[{"start": 0.0, "end":10.0, "speaker": "Speaker1"},...]
   ```
   1. Invoke LLM model to run on the audio file
   
1. Transcription of audio on complete file. Expected output: 
      ```py
      audio_with_timestamps=[{"start": 0.0, "end":10.0, "word": "lalala"},{"start": 10.0, "end":20.0, "word": "lalala"}...]
      ```
   1. Split audio file into 10 second chunks. Expected output: `audio001.wav,audio002.wav...`
   1. Call the Transcript API with each file. Actual output:
      ```py
      audio_with_raw_timestamps=[{"start": 0.0, "end":10.0, "word": "lalala"},{"start": 0.0, "end":10.0, "word": "lalala"}...]
      ```
   1. Call the Transcript API with each file. Actual output:
      ```py
      audio_with_offset_timestamps=[{"start": 0.0, "end":10.0, "word": "lalala"},{"start": 10.0, "end":20.0, "word": "lalala"}...]
      ```
1. Expected output: 
   ```py
   combined_output=[{"start": 0.0, "end":10.0, "speaker": "Speaker1", "word": "lalala"},...]
     ```

[] Clean Notebooks and annotate with markdowns to explain each process 

Curating all text dataset
- [] need to get all the info related to the film ( plot,script, crew, cast, production information)
  - [] Scrape Wikipedia,
  - [] use IMDB pro for getting any missing information
- [] Use the Speaker identification to get all the interviews from youtube processed and stored in csv

Model Trainig
- [] Finalize list of LLMs to be tested
- [] Create metrics for performance testing (f1 score, accuracy, perplexity)
- [] Create a validation set for testing the above metrics



