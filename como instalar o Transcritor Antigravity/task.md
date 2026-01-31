# Debugging Transcription Display Issue

## Problem
When a new audio file is saved to the monitored folder, the application shows "[14:43:37] Novo arquivo processado:" but doesn't display the transcription text.

## Task Breakdown

- [x] Analyze the issue
  - [x] Identify that `append_text()` is called with empty or missing transcription data
  - [x] Add debug logging to track the transcription flow
- [x] Fix the problem
  - [x] Add error handling and logging in `format_diarized_transcript()`
  - [x] Add logging in `process_file()` to track API response
  - [x] Ensure transcription data is properly passed through the queue
- [x] Test the solution
  - [x] Create a test audio file
  - [x] Verify transcription appears correctly
