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
uvicorn app.main:app --port 8000 --reload

Terminal 2: Run the Mock Notes Service
Navigate to the mock_services directory and run the first mock tool:

Bash
uvicorn mock_notes_service:app --port 8001 --reload

Terminal 3: Run the Mock Flashcards Service
In another terminal, navigate to the mock_services directory and run the second mock tool:

Bash
uvicorn mock_flashcards_service:app --port 8002 --reload

Terminal 4: Run the Mock Concept Explainer Service
Finally, in a fourth terminal, navigate to the mock_services directory and run the last mock tool:

Bash
uvicorn mock_concept_service:app --port 8003 --reload

With all four services running, the entire system is now live and ready for the testing.

Step 3: Perform the test using FastAPI's Interactive UI
This is the easiest and most visual way to conduct your demo.

Open your web browser and navigate to http://127.0.0.1:8000/docs.

You will see the FastAPI Swagger UI for your orchestrator.

Expand the POST /v1/chat endpoint.

Click the "Try it out" button.

You will see a text box for the "Request body". Delete the existing content and paste the JSON payloads from the demo_scenarios.md file for each scenario you want to demonstrate.

Click the "Execute" button to send the request to your orchestrator and see the live response.

Follow the scenarios in the demo_scenarios.md file to showcase the full capabilities of your system.