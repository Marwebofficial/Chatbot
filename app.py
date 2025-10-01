import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App and enable CORS
app = Flask(__name__)
# Allow cross-origin requests from the frontend if it's running on a different port/domain
CORS(app) 

# Configure the Gemini API client
# The client automatically looks for the GEMINI_API_KEY environment variable.
try:
    client = genai.Client()
    # The model we will use for a fast chat experience
    MODEL = 'gemini-2.5-flash'
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    # You should handle this more robustly in a production app

@app.route('/')
def index():
    """Renders the main chat interface template."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint to handle incoming user messages and return an AI response."""
    try:
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Call the Gemini API to generate content
        response = client.models.generate_content(
            model=MODEL,
            contents=[user_message]
        )
        
        # Extract the text response
        ai_response = response.text
        
        return jsonify({'response': ai_response})

    except APIError as e:
        # Handle specific API errors (e.g., invalid key, rate limits)
        return jsonify({'error': f'Gemini API Error: {e.message}'}), 500
    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # Create a simple .env file in your project root with your API key:
    # GEMINI_API_KEY="YOUR_API_KEY_HERE"
    if not os.getenv('GEMINI_API_KEY'):
        print("WARNING: GEMINI_API_KEY not found. Please set it in a .env file or environment.")

    # Run the Flask app
    app.run(debug=True)