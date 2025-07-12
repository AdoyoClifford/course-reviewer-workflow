from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import json
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active sessions (in production, use a proper database)
active_sessions = {}

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/create-session', methods=['POST'])
def create_session():
    """Create a new evaluation session"""
    try:
        # For demo purposes, we'll use a simple session ID
        # In production, integrate with the actual remote deployment
        session_id = f"demo_session_{len(active_sessions) + 1}"
        
        active_sessions[session_id] = {
            'id': session_id,
            'status': 'active',
            'created_at': str(os.times())
        }
        
        logger.info(f"Created session: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_course():
    """Analyze course content using the Course Reviewer Workflow"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        course_content = data.get('content')
        
        if not session_id or not course_content:
            return jsonify({
                'success': False,
                'error': 'Missing session_id or content'
            }), 400
        
        if session_id not in active_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session_id'
            }), 400
        
        logger.info(f"Analyzing content for session: {session_id}")
        
        # Get the deployed resource ID (use the one we found earlier)
        resource_id = os.getenv('COURSE_REVIEWER_RESOURCE_ID', 'projects/319361346283/locations/us-central1/reasoningEngines/856273267432882176')
        
        # Call the actual Course Reviewer Workflow
        results = call_course_reviewer_workflow(resource_id, session_id, course_content)
        
        # If the workflow call failed, return an error
        if results is None:
            return jsonify({
                'success': False,
                'error': 'Failed to analyze course content using the deployed workflow'
            }), 500
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error analyzing course: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def call_course_reviewer_workflow(resource_id, session_id, course_content):
    """
    Call the actual Course Reviewer Workflow deployed on Google Cloud
    This function integrates with the remote deployment
    """
    try:
        import subprocess
        import json
        import re
        
        logger.info(f"Calling deployed workflow with resource_id: {resource_id}")
        
        # Use the .venv Python executable directly with absl
        python_path = os.path.join('..', '.venv', 'Scripts', 'python.exe')
        
        # First, create a session if needed (or use existing one)
        create_session_command = [
            python_path, '-m', 'deployment.remote', 
            '--create_session',
            f'--resource_id={resource_id}'
        ]
        
        logger.info("Creating session for workflow...")
        session_result = subprocess.run(create_session_command, capture_output=True, text=True, cwd='..')
        
        if session_result.returncode != 0:
            logger.error(f"Failed to create session: {session_result.stderr}")
            logger.error(f"Session stdout: {session_result.stdout}")
            return None
        
        # Extract session ID from output
        session_output = session_result.stdout
        session_id_match = re.search(r'Session ID: (\d+)', session_output)
        
        if not session_id_match:
            logger.error("Could not extract session ID from output")
            logger.error(f"Full output: {session_output}")
            return None
        
        actual_session_id = session_id_match.group(1)
        logger.info(f"Created session with ID: {actual_session_id}")
        
        # Now send the course content for analysis
        analyze_command = [
            python_path, '-m', 'deployment.remote',
            '--send',
            f'--resource_id={resource_id}',
            f'--session_id={actual_session_id}',
            f'--message={course_content}'
        ]
        
        logger.info("Sending course content for analysis...")
        result = subprocess.run(analyze_command, capture_output=True, text=True, cwd='..')
        
        if result.returncode != 0:
            logger.error(f"Workflow execution failed: {result.stderr}")
            logger.error(f"Workflow stdout: {result.stdout}")
            return None
        
        # Parse the output to extract the evaluation results
        output = result.stdout
        logger.info(f"Workflow output received: {len(output)} characters")
        
        # Look for the final JSON result from the score calculator
        # The output should contain a JSON object with the final evaluation
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for lines that contain JSON-like content with final_score
            if 'final_score' in line and '{' in line:
                try:
                    # Extract JSON from the line
                    start_idx = line.find('{')
                    end_idx = line.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = line[start_idx:end_idx]
                        
                        # Clean up any markdown formatting
                        json_str = json_str.replace('```json', '').replace('```', '')
                        
                        # Parse the JSON
                        evaluation_result = json.loads(json_str)
                        
                        # Validate that it has the expected structure
                        if 'final_score' in evaluation_result and 'individual_scores' in evaluation_result:
                            logger.info(f"Successfully parsed evaluation result: {evaluation_result['final_score']}")
                            return evaluation_result
                            
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON from line: {e}")
                    continue
        
        # If we couldn't parse the results, log the output for debugging
        logger.warning("Could not parse workflow results from output:")
        logger.warning(output)
        return None
        
    except Exception as e:
        logger.error(f"Error calling workflow: {str(e)}")
        return None

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions"""
    return jsonify({
        'success': True,
        'sessions': list(active_sessions.values())
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Course Reviewer Web UI'
    })

if __name__ == '__main__':
    # Check if we're in the web-ui directory
    current_dir = os.path.basename(os.getcwd())
    if current_dir != 'web-ui':
        print("Please run this server from the web-ui directory:")
        print("cd web-ui && python server.py")
        exit(1)
    
    print("Starting Course Reviewer Web UI Server...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
