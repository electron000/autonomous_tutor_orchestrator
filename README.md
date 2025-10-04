Step 1: Set Up the Environment

A. Create a .env file:
First, in the root directory of my project, we need to create a .env file and add the Google API key:

GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

B. Place the Mock Services:
To simulate the external tools my orchestrator calls, I've created three simple mock services. We'll save these Python files (mock_notes_service.py, mock_flashcards_service.py, mock_concept_service.py) into a new mock_services directory.

C. Install Dependencies:
The mock services require uvicorn and fastapi. If they aren't already installed, we can add them with pip:

Bash

pip install requirements.txt

Step 2: Run All the Services
To get the full system running, we need to launch four separate processes in four different terminals. 

Terminal 1: Run My Orchestrator App
Navigate to the project's root directory and run my main application:

Bash
uvicorn main:app --host 0.0.0.0 --port 8000

Terminal 2: Run the Mock Notes Service
Navigate to the mock_services directory and run the first mock tool:

Bash
uvicorn mock_notes_service:app --host 0.0.0.0 --port 8001

Terminal 3: Run the Mock Flashcards Service
In another terminal, navigate to the mock_services directory and run the second mock tool:

Bash
uvicorn mock_flashcards_service:app --host 0.0.0.0 --port 8002

Terminal 4: Run the Mock Concept Explainer Service
Finally, in a fourth terminal, navigate to the mock_services directory and run the last mock tool:

Bash
uvicorn mock_concept_service:app --host 0.0.0.0 --port 8003

With all four services running, the entire system is now live and ready for the testing.