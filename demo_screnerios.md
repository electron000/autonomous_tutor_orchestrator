# Final Demo Scenarios and API Payloads

Use these JSON payloads in the FastAPI UI (`http://127.0.0.1:8000/docs`) to run the definitive demo for the upgraded system.

---

### Scenario 1: Note Maker Tool (Successful Execution)

**Goal:** Show the system correctly executing the `note_maker_tool` with all required parameters and an optional one.

**User Message:** `Can you make me some structured notes on Photosynthesis for my Biology class? Please include examples.`

**Copy and paste this JSON into the request body:**
```json
{
  "user_id": "student-demo-123",
  "conversation_id": "conv-001",
  "message": "Can you make me some structured notes on Photosynthesis for my Biology class? Please include examples.",
  "user_info": {
    "name": "Alex",
    "grade_level": "10",
    "learning_style_summary": "Prefers outlines and structured notes",
    "emotional_state_summary": "Focused and attentive",
    "mastery_level_summary": "Level 6: Good understanding"
  },
  "chat_history": [
    { "role": "user", "content": "Hi there!" },
    { "role": "assistant", "content": "Hello Alex! How can I help you study today?" }
  ]
}
Expected Outcome: The orchestrator will call the note_maker_tool. The mock service will receive include_examples: true and generate a detailed, personalized response, which the orchestrator will then format and return to the user.

Scenario 2: Flashcard Generator (Successful Execution)
Goal: Show the system successfully running the flashcard_generator_tool from a clear, direct user request.

User Message: Create 5 medium-difficulty flashcards about the Solar System for my science class.

Copy and paste this JSON into the request body:

JSON

{
  "user_id": "student-demo-456",
  "conversation_id": "conv-002",
  "message": "Create 5 medium-difficulty flashcards about the Solar System for my science class.",
  "user_info": {
    "name": "Sam",
    "grade_level": "8",
    "learning_style_summary": "Kinesthetic learner, learns best through practice and repetition",
    "emotional_state_summary": "Focused and motivated to improve",
    "mastery_level_summary": "Level 6: Good understanding, ready for application"
  },
  "chat_history": []
}
Expected Outcome: The orchestrator will call the flashcard_generator_tool with count: 5 and difficulty: "medium". The mock service will return a personalized response with 5 flashcards, which the orchestrator will format for the user.

Scenario 3: Concept Explainer (Successful Execution)
Goal: Show the system successfully running the concept_explainer_tool, demonstrating its ability to extract all necessary parameters.

User Message: I don't understand what mitosis is. Can you give me an intermediate explanation? We're covering it in biology.

Copy and paste this JSON into the request body:

JSON

{
  "user_id": "student-demo-789",
  "conversation_id": "conv-003",
  "message": "I don't understand what mitosis is. Can you give me an intermediate explanation? We're covering it in biology.",
  "user_info": {
    "name": "Charlie",
    "grade_level": "9",
    "learning_style_summary": "Auditory learner, prefers simple terms and step-by-step explanations",
    "emotional_state_summary": "Curious and engaged in learning",
    "mastery_level_summary": "Level 4: Building foundational knowledge"
  },
  "chat_history": [
    { "role": "assistant", "content": "We've been discussing cell division. Is there anything you're finding tricky?" }
  ]
}
Expected Outcome: The orchestrator will call the concept_explainer_tool with concept_to_explain: "mitosis" and desired_depth: "intermediate". The mock service will return a detailed, personalized explanation.

Scenario 4: Handling Missing Parameters (Clarification)
Goal: Show the system's ability to handle an ambiguous request, identify missing required parameters, and ask a clarifying question.

User Message: I need to study the periodic table.

Copy and paste this JSON into the request body:

JSON

{
  "user_id": "student-demo-123",
  "conversation_id": "conv-004",
  "message": "I need to study the periodic table.",
  "user_info": {
    "name": "Alex",
    "grade_level": "10",
    "learning_style_summary": "Visual learner",
    "emotional_state_summary": "A bit confused",
    "mastery_level_summary": "Level 5: Developing competence"
  },
  "chat_history": []
}
Expected Outcome: The router will likely select a tool (e.g., note_maker_tool), but the extractor will find a required parameter like subject is missing. The system will respond with a clarifying question, such as: "Sounds good! To help you study the periodic table, what subject are we focusing on, like Chemistry or Physics?"

Scenario 5: No Tool Match (Graceful Fallback)
Goal: Demonstrate that the system can handle general conversation that doesn't map to any specific educational tool.

User Message: Thanks, that was really helpful!

Copy and paste this JSON into the request body:

JSON

{
  "user_id": "student-demo-456",
  "conversation_id": "conv-005",
  "message": "Thanks, that was really helpful!",
  "user_info": {
    "name": "Sam",
    "grade_level": "8",
    "learning_style_summary": "Visual learner",
    "emotional_state_summary": "Pleased",
    "mastery_level_summary": "Level 5: Developing competence"
  },
  "chat_history": [
    { "role": "user", "content": "Can you explain the rock cycle?" },
    { "role": "assistant", "content": "Of course! The rock cycle is..." }
  ]
}
Expected Outcome: The router will determine that no tool is appropriate for this conversational closing. The system will return its polite, generic fallback response, like: "I can't directly answer that, but I can help with other educational tools. What would you like to do?"