# AnnotateVerify

AnnotateVerify is a browser-based tool for reviewing and verifying video annotations. Users can upload videos and corresponding JSON annotation files, review video segments, and confirm or reject assigned labels. Incorrect labels are logged for further analysis.

## Features

- **Video Playback with Annotations**: Play video segments with captions displaying the assigned labels.
- **Verification Buttons**: Provide "Correct" and "Incorrect" buttons for users to confirm or reject labels.
- **Logging Incorrect Labels**: Log incorrect labels with timestamps to an output file.
- **Slider for Video Control**: Allow users to move the video forward or backward using a slider.

## Usage

1. **Upload Video**: Click the "Choose File" button under "Upload Video" and select a video file from your local system.
2. **Upload Annotations**: Click the "Choose File" button under "Upload Annotations" and select a JSON file containing the annotations.
3. **Review and Verify**: Use the "Correct" and "Incorrect" buttons to verify the labels. The tool will log any incorrect labels for further review.
4. **Control Video**: Use the slider to move the video forward or backward.


## Running
To run the application: 
- Clone the repository
- Install the required packages using the following command:

  - `pip3 install -r requirements.txt`
- cd into the direcotry and run the following command:

  `python app.py`
  

## TODO
- [ ] Add support for multiple annotation files
- [ ] Improve logging functionality
- [ ] Add support for different video formats
- [ ] Add support for different annotation formats
- [ ] Add support for different video players
- [ ] Add support for segment-level verification
- [ ] Add support for custom labels
- [ ] Add support to change labels on the fly.