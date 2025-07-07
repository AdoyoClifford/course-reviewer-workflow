
# --- Rubric Data ---
RUBRIC_WEIGHTS = {
    "Blockchain Technology and Development": {
        "Learner Agency": 10, "Critical Thinking": 19, "Collaborative Learning": 10,
        "Reflective Practice": 5, "Adaptive Learning": 9, "Authentic Learning": 14,
        "Technology Integration": 19, "Learner Support": 5, "Assessment for Learning": 5,
        "Engagement and Motivation": 4
    },
    "Web3 Development and Design": {
        "Learner Agency": 15, "Critical Thinking": 15, "Collaborative Learning": 15,
        "Reflective Practice": 10, "Adaptive Learning": 10, "Authentic Learning": 10,
        "Technology Integration": 10, "Learner Support": 5, "Assessment for Learning": 5,
        "Engagement and Motivation": 5
    },
    "Blockchain Applications and Business": {
        "Learner Agency": 10, "Critical Thinking": 20, "Collaborative Learning": 15,
        "Reflective Practice": 10, "Adaptive Learning": 10, "Authentic Learning": 15,
        "Technology Integration": 5, "Learner Support": 5, "Assessment for Learning": 5,
        "Engagement and Motivation": 5
    },
    "Web3 Ecosystem and Operations": {
        "Learner Agency": 16, "Critical Thinking": 16, "Collaborative Learning": 16,
        "Reflective Practice": 10, "Adaptive Learning": 11, "Authentic Learning": 10,
        "Technology Integration": 5, "Learner Support": 5, "Assessment for Learning": 5,
        "Engagement and Motivation": 6
    },
    "Emerging Technologies and Intersections": {
        "Learner Agency": 14, "Critical Thinking": 19, "Collaborative Learning": 14,
        "Reflective Practice": 10, "Adaptive Learning": 10, "Authentic Learning": 14,
        "Technology Integration": 5, "Learner Support": 5, "Assessment for Learning": 4,
        "Engagement and Motivation": 5
    }
}

COURSE_CLUSTERS = list(RUBRIC_WEIGHTS.keys())
EVALUATION_ELEMENTS = list(RUBRIC_WEIGHTS["Blockchain Technology and Development"].keys())
PASS_MARK = 80  # Default, can be overridden