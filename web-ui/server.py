from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import json
from dotenv import load_dotenv
import logging
import subprocess
import re
import ast

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
        
        resource_id = os.getenv('COURSE_REVIEWER_RESOURCE_ID', 'projects/319361346283/locations/us-central1/reasoningEngines/856273267432882176')
        
        results = call_course_reviewer_workflow(resource_id, session_id, course_content)
        
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
    Call the actual Course Reviewer Workflow deployed on Google Cloud.
    """
    try:
        python_path = os.path.join('..', '.venv', 'Scripts', 'python.exe')
        
        create_session_command = [
            python_path, '-m', 'deployment.remote', 
            '--create_session',
            f'--resource_id={resource_id}'
        ]
        
        logger.info("Creating session for workflow...")
        session_result = subprocess.run(create_session_command, capture_output=True, text=True, cwd='..')
        
        if session_result.returncode != 0:
            logger.error(f"Failed to create session: {session_result.stderr}")
            return None
        
        session_id_match = re.search(r'Session ID: (\d+)', session_result.stdout)
        
        if not session_id_match:
            logger.error("Could not extract session ID from output")
            return None
        
        actual_session_id = session_id_match.group(1)
        logger.info(f"Created session with ID: {actual_session_id}")
        
        analyze_command = [
            python_path, '-m', 'deployment.remote',
            '--send',
            f'--resource_id={resource_id}',
            f'--session_id={actual_session_id}',
        ]
        
        logger.info("Sending course content for analysis via stdin...")
        result = subprocess.run(
            analyze_command, 
            capture_output=True, 
            encoding='utf-8', 
            cwd='..',
            input=course_content
        )
        
        if result.returncode != 0:
            logger.error(f"Workflow execution failed: {result.stderr}")
            return None
        
        output = result.stdout
        logger.info(f"Workflow output received: {len(output)} characters")
        
        lines = output.strip().split('\n')
        score_calculator_output_str = None
        for line in lines:
            if "'author': 'score_calculator'" in line:
                score_calculator_output_str = line.strip()
                break
        
        if not score_calculator_output_str:
            logger.warning("Could not find output from score_calculator agent.")
            return None

        try:
            event_dict = ast.literal_eval(score_calculator_output_str)
            json_str = event_dict['content']['parts'][0]['text']
            
            # Clean up markdown formatting
            json_str = re.sub(r'^```json\s*', '', json_str, flags=re.MULTILINE)
            json_str = re.sub(r'\s*```$', '', json_str, flags=re.MULTILINE)
            
            evaluation_result = json.loads(json_str)
            
            if 'final_score' in evaluation_result:
                logger.info(f"Successfully parsed evaluation result: {evaluation_result['final_score']}")
                return evaluation_result
            else:
                logger.warning("Parsed JSON does not contain 'final_score'.")
                return None

        except (ValueError, SyntaxError, KeyError, IndexError) as e:
            logger.error(f"Failed to parse workflow output: {e}")
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
    current_dir = os.path.basename(os.getcwd())
    if current_dir != 'web-ui':
        print("Please run this server from the web-ui directory:")
        print("cd web-ui && python server.py")
        exit(1)
    
    print("Starting Course Reviewer Web UI Server...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)