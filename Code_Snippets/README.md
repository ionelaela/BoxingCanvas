# *Boxing Canvas — Selected Code Snippets*

This folder contains a small, curated selection of implementation excerpts from *Boxing Canvas*, a full-stack generative-art project that transforms webcam-detected hand movements into visual compositions.

## *Selected implementation areas*

| File | What it demonstrates |
|---|---|
| [01_hand_tracking_and_motion.py](01_hand_tracking_and_motion.py) | MediaPipe hand landmarks and frame-to-frame movement measurement |
| [02_punch_recognition.py](02_punch_recognition.py) | Experimental punch classification using movement direction |
| [03_generative_art_engine.py](03_generative_art_engine.py) | Procedural strokes, color mapping, particles, and artwork export |
| [Authentication/04_google_token_verification.py](Authentication/04_google_token_verification.py) | Server-side Google ID token verification and session creation |
| [Authentication/05_canvas_access_control.py](Authentication/05_canvas_access_control.py) | Canvas ownership, account association, and authorization checks |

## *Technical notes*

- The hand-tracking excerpt uses MediaPipe Tasks in video mode and tracks the index fingertip landmark.
- Movement is measured as frame-to-frame displacement in image pixels.
- Punch classification is a heuristic prototype based on horizontal and vertical movement. It is not a trained boxing-action recognition model.
- The current movement score is pixel displacement, not physical speed in km/h.
- The authentication excerpts are selected parts of the FastAPI backend and depend on helper functions defined in the original application. They are intended to demonstrate the implementation, not to run independently.

## *Dependencies represented*

Python, OpenCV, MediaPipe, NumPy, FastAPI, Pydantic, and Google Auth.

## *Security*

No credentials, OAuth client secrets, private keys, session secrets, access tokens, personal databases, or session data are included in these excerpts. Never publish those files or values in the repository.
