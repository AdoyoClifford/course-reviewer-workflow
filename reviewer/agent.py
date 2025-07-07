from google.adk.agents import SequentialAgent, LlmAgent
from .course_categorizer.agent import course_categorizer_agent
from .course_grader.agent import course_grader_agent
from .score_calculator.agent import score_calculator_agent

# Create the evaluation pipeline
course_evaluation_pipeline = SequentialAgent(
    name='CourseEvaluationPipeline',
    description='A comprehensive course evaluation pipeline that categorizes, grades, and calculates scores for educational content.',
    sub_agents=[
        course_categorizer_agent,
        course_grader_agent,
        score_calculator_agent
    ]
)

root_agent = course_evaluation_pipeline

