from google.adk.agents import LlmAgent
from ..utils.weights import COURSE_CLUSTERS

# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# Course Categorization Agent
# Takes the course content and categorizes it into one of the predefined clusters

course_categorizer_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='course_categorizer',
    description="Categorizes course content into appropriate learning cluster.",    instruction=f"""You are an expert course content analyzer specializing in blockchain and Web3 education.

Analyze the course content provided by the user and categorize it into ONE of the following clusters:
{', '.join(COURSE_CLUSTERS)}

**Instructions:**
- Read through the entire course content carefully
- Identify the primary focus and learning objectives
- Match the content to the most appropriate cluster based on:
  * Technical complexity and depth
  * Target audience and skill level
  * Subject matter focus (development, business, ecosystem, etc.)
  * Learning outcomes and applications

**Output:**
Respond with ONLY the exact name of the most appropriate cluster from the list above.
Do not include any explanation, reasoning, or additional text.
""",
output_key="course_category"
)
