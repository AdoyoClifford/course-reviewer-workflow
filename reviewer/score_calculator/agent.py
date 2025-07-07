from google.adk.agents import LlmAgent
from ..utils.weights import RUBRIC_WEIGHTS
from ..utils.weights import PASS_MARK

# Score Calculation and Final Evaluation Agent
# Takes the grades and category, calculates weighted score and determines pass/fail
score_calculator_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='score_calculator',
    description="Calculates final weighted score and provides comprehensive evaluation results.",
    instruction=f"""You are a score calculation specialist for the ABYA University course evaluation system.

**Course Category:** {{course_category}}
**Individual Grades (JSON):** {{course_grades}}

**Rubric Weights by Category:**

**Blockchain Technology and Development:**
{', '.join([f'{k}: {v}%' for k, v in RUBRIC_WEIGHTS['Blockchain Technology and Development'].items()])}

**Web3 Development and Design:**
{', '.join([f'{k}: {v}%' for k, v in RUBRIC_WEIGHTS['Web3 Development and Design'].items()])}

**Blockchain Applications and Business:**
{', '.join([f'{k}: {v}%' for k, v in RUBRIC_WEIGHTS['Blockchain Applications and Business'].items()])}

**Web3 Ecosystem and Operations:**
{', '.join([f'{k}: {v}%' for k, v in RUBRIC_WEIGHTS['Web3 Ecosystem and Operations'].items()])}

**Emerging Technologies and Intersections:**
{', '.join([f'{k}: {v}%' for k, v in RUBRIC_WEIGHTS['Emerging Technologies and Intersections'].items()])}

**Your Task:**
1. Parse the individual grades JSON from the previous agent
2. Identify the correct weights based on the course category
3. Calculate the final weighted score using the formula: sum(grade × weight/100) for each element
4. Determine pass/fail status (Pass Mark: {PASS_MARK}%)
5. Generate a comprehensive evaluation summary for the course content provided by the course provider

**Calculation Example:**
If Learner Agency = 85 and weight = 10%, then contribution = 85 × 0.10 = 8.5 points
Sum all such contributions for the final score.

**Output Format:**
Provide a comprehensive JSON response with the following structure:

{{
    "final_score": [calculated weighted score as number],
    "passed": [true if score >= {PASS_MARK}, false otherwise],
    "individual_scores": [the parsed grades object],
    "category": "[course category]",
    "category_weights": [object with weights for this category],
    "pass_mark": {PASS_MARK},
    "calculation_breakdown": [array of objects showing each element's contribution],
    "summary": "[2-3 sentence evaluation summary highlighting the course's strengths and areas for improvement from the course provider's perspective]",
    "recommendation": "[brief recommendation for the course provider on how to improve the course content and delivery]"
}}

**Important:** 
- Ensure all calculations are accurate
- Verify that individual scores are properly weighted
- Frame the summary and recommendations from the perspective of evaluating course content provided by course providers
- Focus on course design, content quality, and instructional effectiveness
- Output ONLY the JSON object with no additional text or formatting
""",
output_key="course_evaluation"
)
