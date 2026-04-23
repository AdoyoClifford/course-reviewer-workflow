<div align="center">

# 🤖 Course Reviewer Workflow

**AI-powered course evaluation system using Google ADK & Vertex AI**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![Vertex AI](https://img.shields.io/badge/Vertex%20AI-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Gemini](https://img.shields.io/badge/Gemini%202.0-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)

</div>

---

## 📖 About

An AI-powered course evaluation system built with **Google's Agent Development Kit (ADK)** and **Vertex AI**. This system provides comprehensive automated evaluation of educational content using ABYA University's standardized rubric, specifically designed for blockchain and Web3 courses.

## ✨ Features

- 📂 **Automated Categorization** — Classifies courses into 5 specialized clusters
- 📝 **Comprehensive Evaluation** — Assesses 10 key educational elements using ABYA University rubric
- ⚖️ **Weighted Scoring** — Category-specific importance weighting for accurate assessment
- ✅ **Pass/Fail Determination** — 80% threshold with detailed feedback
- 🔗 **Multi-Agent Pipeline** — Sequential AI agents for categorization, grading, and score calculation
- ☁️ **Cloud Deployment** — Scalable deployment on Google Cloud Vertex AI
- 👥 **Session Management** — Multi-user support with persistent sessions

## 🏗️ Architecture

The system implements a **Sequential Agent Pipeline** with three specialized agents:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    STAGE 1       │     │    STAGE 2       │     │    STAGE 3       │
│                 │     │                 │     │                 │
│  📂 Course      │────▶│  📝 Course      │────▶│  🧮 Score       │
│  Categorizer    │     │  Grader         │     │  Calculator     │
│                 │     │                 │     │                 │
│  Classifies     │     │  Evaluates 10   │     │  Applies weights│
│  into 5         │     │  rubric         │     │  & calculates   │
│  clusters       │     │  elements       │     │  final score    │
│                 │     │  (0-100 each)   │     │  (pass ≥ 80%)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘

                    All powered by Gemini 2.0 Flash
```

### Agent Details

| Agent | Purpose | Output |
|---|---|---|
| **Course Categorizer** | Classifies course into specialized clusters | Category classification |
| **Course Grader** | Evaluates against 10 ABYA rubric elements | JSON with scores (0-100) |
| **Score Calculator** | Calculates weighted scores & final evaluation | Comprehensive results + recommendations |

## 📊 Evaluation Rubric

The system grades courses on **10 educational elements**:

| Element | Description |
|---|---|
| 🎯 Learner Agency | Empowerment of learner control |
| 🧠 Critical Thinking | Analytical reasoning and problem-solving |
| 🤝 Collaborative Learning | Peer learning and group work |
| 🪞 Reflective Practice | Self-reflection and metacognitive awareness |
| 🔄 Adaptive Learning | Accommodation of different learning styles |
| 🌍 Authentic Learning | Real-world, meaningful experiences |
| 💻 Technology Integration | Effective use of technology |
| 🛟 Learner Support | Guidance and assistance provided |
| 📋 Assessment for Learning | Formative assessment quality |
| 🔥 Engagement & Motivation | Course engagement level |

### Course Categories & Weight Distribution

| Category | Top Weighted Elements |
|---|---|
| **Blockchain Technology & Development** | Critical Thinking (19%), Tech Integration (19%), Authentic Learning (14%) |
| **Web3 Development & Design** | Balanced: Agency, Critical Thinking, Collaborative Learning (15% each) |
| **Blockchain Applications & Business** | Critical Thinking (20%), Authentic Learning (15%), Collaborative (15%) |
| **Web3 Ecosystem & Operations** | Agency (16%), Critical Thinking (16%), Collaborative Learning (16%) |
| **Emerging Technologies** | Critical Thinking (19%), Agency (14%), Authentic Learning (14%) |

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Language** | Python 3.12+ |
| **AI Framework** | Google Agent Development Kit (ADK) |
| **LLM** | Gemini 2.0 Flash |
| **Cloud** | Google Cloud Vertex AI |
| **Package Manager** | Poetry |
| **Frontend** | Web UI (included) |

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **Poetry** — [Install Poetry](https://python-poetry.org/docs/#installation)
- **Google Cloud account** with Vertex AI API enabled
- **Google Cloud CLI** — [Install gcloud](https://cloud.google.com/sdk/docs/install)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdoyoClifford/course-reviewer-workflow.git
   cd course-reviewer-workflow
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**
   ```bash
   source $(poetry env info --path)/bin/activate
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your credentials:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STAGING_BUCKET=gs://your-bucket-name
   GOOGLE_API_KEY=your-google-api-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

   > ⚠️ **Never commit your `.env` file to version control!**

5. **Set up Google Cloud authentication**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   gcloud services enable aiplatform.googleapis.com
   ```

## 🧪 Usage

### Local Testing

```bash
poetry run deploy-local
```

This will initialize the agent, create a test session, run a sample evaluation, and display results.

### Remote Deployment

```bash
# Deploy to Google Cloud
poetry run deploy-remote --create

# List all deployments
poetry run deploy-remote --list

# Create a session
poetry run deploy-remote --create_session --resource_id=<id>

# Send course for evaluation
poetry run deploy-remote --send \
  --resource_id=<id> \
  --session_id=<session-id> \
  --message="[Your course content here]"

# Clean up
poetry run deploy-remote --delete --resource_id=<id>
```

### Example

**Input:**
```
"This course covers blockchain fundamentals, including cryptographic hashing,
consensus mechanisms, smart contracts, and practical development using Solidity.
Students will build a complete DeFi application..."
```

**Output:**
```json
{
  "final_score": 84.2,
  "passed": true,
  "category": "Blockchain Technology and Development",
  "individual_scores": {
    "Learner Agency": 85,
    "Critical Thinking": 90,
    "Collaborative Learning": 78
  },
  "summary": "Strong technical course with excellent critical thinking components...",
  "recommendation": "Consider adding more collaborative learning opportunities..."
}
```

## 📁 Project Structure

```
course-reviewer-workflow/
├── reviewer/                    # Main package
│   ├── __init__.py              # ADK app definition
│   ├── agent.py                 # Root agent pipeline
│   ├── course_categorizer/      # Stage 1: Categorization
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── course_grader/           # Stage 2: Grading
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── score_calculator/        # Stage 3: Score calculation
│   │   ├── __init__.py
│   │   └── agent.py
│   └── utils/
│       └── weights.py           # Rubric weights & configs
├── deployment/                  # Deployment scripts
│   ├── local.py                 # Local testing
│   ├── remote.py                # Cloud deployment
│   └── cleanup.py               # Cleanup utility
├── web-ui/                      # Web interface
├── .env.example                 # Environment template
├── pyproject.toml               # Project configuration
├── poetry.lock
└── README.md
```

## 🔧 Troubleshooting

<details>
<summary><b>Authentication issues</b></summary>

- Ensure you're logged in: `gcloud auth login`
- Verify project ID and location in `.env`
- Check Vertex AI API is enabled
- Confirm API keys are correctly set
</details>

<details>
<summary><b>Deployment failures</b></summary>

- Check the staging bucket exists and is accessible
- Verify all required environment variables are set
- Ensure necessary Google Cloud permissions
- Run `poetry install` to verify dependencies
</details>

<details>
<summary><b>Evaluation errors</b></summary>

- Verify course content is provided as a string
- Check all agents are properly configured
- Ensure Gemini 2.0 Flash is available in your region
- Review agent logs for specific errors
</details>

<details>
<summary><b>Web UI analysis fails</b></summary>

- If UI shows "Analysis failed" but terminal works, the issue is server-to-script communication. Fixed by using `stdin` to pass course content.
</details>

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test locally and remotely
5. Update documentation
6. Submit a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by [Adoyo Clifford](https://github.com/AdoyoClifford)**

</div>
