# Course Reviewer Workflow

An AI-powered course evaluation system built with Google's Agent Development Kit (ADK) and Vertex AI. This system provides comprehensive automated evaluation of educational content using ABYA University's standardized rubric, specifically designed for blockchain and Web3 courses.

## Features

- **Automated Course Categorization**: Classifies courses into 5 specialized clusters
- **Comprehensive Evaluation**: Assesses 10 key educational elements using ABYA University rubric
- **Weighted Scoring**: Category-specific importance weighting for accurate assessment
- **Pass/Fail Determination**: 80% threshold with detailed feedback
- **Multi-Agent Pipeline**: Sequential AI agents for categorization, grading, and score calculation
- **Cloud Deployment**: Scalable deployment on Google Cloud Vertex AI
- **Session Management**: Multi-user support with persistent sessions

## Prerequisites

- Python 3.12+
- Poetry (Python package manager)
- Google Cloud account with Vertex AI API enabled
- Google Cloud CLI (`gcloud`) installed and authenticated
  - Follow the [official installation guide](https://cloud.google.com/sdk/docs/install) to install gcloud
  - After installation, run `gcloud init` and `gcloud auth login`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd course-reviewer-workflow
```

2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install project dependencies:
```bash
poetry install
```

4. Activate the virtual environment:
```bash
source $(poetry env info --path)/bin/activate
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-location  # e.g., us-central1
GOOGLE_CLOUD_STAGING_BUCKET=gs://your-bucket-name
GOOGLE_API_KEY=your-google-api-key
GEMINI_API_KEY=your-gemini-api-key
```

2. Set up Google Cloud authentication:
```bash
gcloud auth login
gcloud config set project your-project-id
```

3. Enable required APIs:
```bash
gcloud services enable aiplatform.googleapis.com
```

## How It Works

The Course Reviewer Workflow uses a **three-stage sequential agent pipeline**:

### 1. Course Categorization
Analyzes course content and categorizes it into one of five specialized clusters:
- **Blockchain Technology and Development**: Technical blockchain fundamentals
- **Web3 Development and Design**: Web3 application development
- **Blockchain Applications and Business**: Business applications and use cases
- **Web3 Ecosystem and Operations**: Ecosystem management and operations
- **Emerging Technologies and Intersections**: Advanced and emerging topics

### 2. Course Grading
Evaluates the course against 10 ABYA University rubric elements:
- **Learner Agency** (0-100): Empowerment of learner control
- **Critical Thinking** (0-100): Analytical reasoning and problem-solving
- **Collaborative Learning** (0-100): Peer learning and group work
- **Reflective Practice** (0-100): Self-reflection and metacognitive awareness
- **Adaptive Learning** (0-100): Accommodation of different learning styles
- **Authentic Learning** (0-100): Real-world, meaningful experiences
- **Technology Integration** (0-100): Effective use of technology
- **Learner Support** (0-100): Guidance and assistance provided
- **Assessment for Learning** (0-100): Formative assessment quality
- **Engagement and Motivation** (0-100): Course engagement level

### 3. Score Calculation
- Applies category-specific weights to individual scores
- Calculates final weighted score
- Determines pass/fail status (80% threshold)
- Provides comprehensive evaluation summary and improvement recommendations

## Usage

### Local Testing

1. Test the course evaluation pipeline locally:
```bash
poetry run deploy-local
```

This will:
- Initialize the local agent
- Create a test session
- Run a sample course evaluation
- Display the complete evaluation results

### Remote Deployment

1. **Deploy the agent to Google Cloud:**
```bash
poetry run deploy-remote --create
```

2. **List all deployments:**
```bash
poetry run deploy-remote --list
```

3. **Create a session:**
```bash
poetry run deploy-remote --create_session --resource_id=your-resource-id
```

4. **List sessions for a user:**
```bash
poetry run deploy-remote --list_sessions --resource_id=your-resource-id --user_id=your-user-id
```

5. **Send course content for evaluation:**
```bash
poetry run deploy-remote --send --resource_id=your-resource-id --session_id=your-session-id --message="[Your course content here]"
```

6. **Clean up (delete deployment):**
```bash
poetry run deploy-remote --delete --resource_id=your-resource-id
```

### Alternative Commands

You can also use the defined console scripts:
```bash
# Local deployment
deploy-local

# Remote deployment operations
deploy-remote --list
deploy-remote --create
deploy-remote --delete --resource_id=your-resource-id

# Cleanup utility
cleanup
```

## Example Usage

To evaluate a course, send the complete course content as a message. The system will:

1. **Categorize** the course into the appropriate cluster
2. **Grade** each of the 10 evaluation elements (0-100)
3. **Calculate** the final weighted score
4. **Determine** pass/fail status
5. **Provide** detailed feedback and recommendations

**Sample Input:**
```
"This course covers blockchain fundamentals, including cryptographic hashing, 
consensus mechanisms, smart contracts, and practical development using Solidity. 
Students will build a complete DeFi application..."
```

**Sample Output:**
```json
{
    "final_score": 84.2,
    "passed": true,
    "category": "Blockchain Technology and Development",
    "individual_scores": {
        "Learner Agency": 85,
        "Critical Thinking": 90,
        "Collaborative Learning": 78,
        // ... other scores
    },
    "summary": "Strong technical course with excellent critical thinking components...",
    "recommendation": "Consider adding more collaborative learning opportunities..."
}
```

## Project Structure

```
course-reviewer-workflow/
├── reviewer/                     # Main package directory
│   ├── __init__.py              # ADK app definition
│   ├── agent.py                 # Root agent pipeline
│   ├── course_categorizer/      # Course categorization agent
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── course_grader/           # Course grading agent
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── score_calculator/        # Score calculation agent
│   │   ├── __init__.py
│   │   └── agent.py
│   └── utils/                   # Utility modules
│       └── weights.py           # Rubric weights and configurations
├── deployment/                  # Deployment scripts
│   ├── local.py                # Local testing script
│   ├── remote.py               # Remote deployment script
│   └── cleanup.py              # Cleanup utility
├── .env                        # Environment variables
├── poetry.lock                 # Poetry lock file
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Agent Architecture

The system implements a **Sequential Agent Pipeline** with three specialized agents:

### 1. Course Categorizer Agent
- **Model**: Gemini 2.0 Flash
- **Purpose**: Categorizes course content into specialized clusters
- **Output**: Course category classification

### 2. Course Grader Agent  
- **Model**: Gemini 2.0 Flash
- **Purpose**: Evaluates course against 10 ABYA University rubric elements
- **Output**: JSON object with individual scores (0-100)

### 3. Score Calculator Agent
- **Model**: Gemini 2.0 Flash
- **Purpose**: Calculates weighted scores and final evaluation
- **Output**: Comprehensive evaluation results with recommendations

## Rubric Weights by Category

Different course categories have different weightings for the 10 evaluation elements:

**Blockchain Technology and Development:**
- Critical Thinking: 19%, Technology Integration: 19%, Authentic Learning: 14%

**Web3 Development and Design:**
- Balanced approach: 15% each for Agency, Critical Thinking, Collaborative Learning

**Blockchain Applications and Business:**
- Critical Thinking: 20%, Authentic Learning: 15%, Collaborative Learning: 15%

**Web3 Ecosystem and Operations:**
- Agency: 16%, Critical Thinking: 16%, Collaborative Learning: 16%

**Emerging Technologies and Intersections:**
- Critical Thinking: 19%, Agency: 14%, Authentic Learning: 14%

## Development

To extend or modify the evaluation system:

1. **Adding New Course Categories:**
   - Update `COURSE_CLUSTERS` in `reviewer/utils/weights.py`
   - Add corresponding weights in `RUBRIC_WEIGHTS`
   - Update agent prompts to include new categories

2. **Modifying Evaluation Elements:**
   - Update the course grader agent prompt in `reviewer/course_grader/agent.py`
   - Adjust weights in `reviewer/utils/weights.py`
   - Update score calculator logic if needed

3. **Testing Changes:**
   - Test locally using `poetry run deploy-local`
   - Deploy to remote using `poetry run deploy-remote --create`
   - Update documentation as needed

4. **Adding New Agents:**
   - Create new agent in appropriate subdirectory
   - Update the pipeline in `reviewer/agent.py`
   - Add to sequential agent list

## API Integration

The system can be integrated into educational platforms via:

- **Direct Python imports**: Import and use the agent pipeline
- **REST API**: Deploy to Google Cloud and access via HTTP
- **Streaming responses**: Real-time evaluation progress
- **Session management**: Multi-user concurrent evaluations

## Troubleshooting

1. **Authentication issues:**
   - Ensure you're logged in with `gcloud auth login`
   - Verify your project ID and location in `.env`
   - Check that the Vertex AI API is enabled
   - Confirm API keys are correctly set

2. **Deployment failures:**
   - Check the staging bucket exists and is accessible
   - Verify all required environment variables are set
   - Ensure you have the necessary permissions in your Google Cloud project
   - Check Poetry dependencies are installed: `poetry install`

3. **Evaluation errors:**
   - Verify course content is provided as a string message
   - Check that all agents are properly configured
   - Ensure the model (Gemini 2.0 Flash) is available in your region
   - Review agent logs for specific error messages

4. **Cleanup issues:**
   - Use `poetry run cleanup` to remove failed deployments
   - Check Google Cloud Console for orphaned resources
   - Verify resource IDs when deleting specific deployments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally and remotely
5. Update documentation
6. Submit a pull request

## License

[Your chosen license]