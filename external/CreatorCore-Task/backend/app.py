from flask import Flask, request, jsonify
import json
from datetime import datetime
from db_utils import insert_generation, get_latest, update_feedback
from prompts import story_prompt, ad_script_prompt, podcast_script_prompt
from embeddings_utils import generate_embedding, store_embedding, find_similar_generations
import os

app = Flask(__name__)   # <-- Flask app created here

@app.route('/')
def home():
    return "✅ CreatorCore Context Intelligence Backend is running successfully!"


# Load schema
with open('utils/schema.json', 'r') as f:
    schema = json.load(f)

# Mock Gemini integration (replace with actual LangChain + Gemini later)
def mock_generate_with_gemini(prompt_template, topic, goal):
    """
    Mock function to simulate Gemini API call.
    Replace with actual LangChain implementation.
    """
    # Simulate different outputs based on prompt type
    if "story" in prompt_template.template.lower():
        output = f"Generated story for topic '{topic}' with goal '{goal}'."
    elif "ad" in prompt_template.template.lower():
        output = f"Generated ad script for topic '{topic}' with goal '{goal}'."
    elif "podcast" in prompt_template.template.lower():
        output = f"Generated podcast script for topic '{topic}' with goal '{goal}'."
    else:
        output = f"Generated content for topic '{topic}' with goal '{goal}'."

    return {
        "output_text": output,
        "tokens_used": len(output.split()) * 2  # Mock token count
    }

@app.route('/generate', methods=['POST'])
def generate():
    """
    POST /generate
    Triggers Gemini prompt (mocked) and logs the generation.
    Expected JSON: {"topic": "string", "goal": "string", "type": "story|ad|podcast"}
    """
    data = request.get_json()
    if not data or 'topic' not in data or 'goal' not in data:
        return jsonify({"error": "Missing topic or goal"}), 400

    topic = data['topic']
    goal = data['goal']
    gen_type = data.get('type', 'story')  # Default to story

    # Select prompt template
    if gen_type == 'story':
        prompt = story_prompt
    elif gen_type == 'ad':
        prompt = ad_script_prompt
    elif gen_type == 'podcast':
        prompt = podcast_script_prompt
    else:
        return jsonify({"error": "Invalid type. Use 'story', 'ad', or 'podcast'"}), 400

    # Generate content (mocked)
    result = mock_generate_with_gemini(prompt, topic, goal)

    # Prepare data for logging
    log_data = {
        "topic": topic,
        "goal": goal,
        "output_text": result["output_text"],
        "tokens_used": result["tokens_used"]
    }

    # Insert into database
    generation_id = insert_generation(log_data)

    # Generate and store embedding for the output
    embedding = generate_embedding(result["output_text"])
    store_embedding(generation_id, embedding)

    # Find related context (top-3 similar generations)
    related_context = find_similar_generations(embedding, topic=topic, top_k=3, score_weight=0.1)

    return jsonify({
        "id": generation_id,
        "topic": topic,
        "output_text": result["output_text"],
        "tokens_used": result["tokens_used"],
        "related_context": related_context
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    POST /feedback
    Updates feedback for a generation.
    Expected JSON: {"id": "string", "feedback": "string"}
    """
    data = request.get_json()
    if not data or 'id' not in data or 'feedback' not in data:
        return jsonify({"error": "Missing id or feedback"}), 400

    generation_id = data['id']
    feedback_text = data['feedback']

    success = update_feedback(generation_id, feedback_text)

    if success:
        return jsonify({"message": "Feedback updated successfully"})
    else:
        return jsonify({"error": "Failed to update feedback"}), 500

@app.route('/history/<topic>', methods=['GET'])
def history(topic):
    """
    GET /history/<topic>
    Fetches past generations for a topic.
    """
    latest = get_latest(topic)
    if latest:
        return jsonify(latest)
    else:
        return jsonify({"error": "No generations found for this topic"}), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

