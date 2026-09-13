import json

from app.services.groq_service import client


def evaluate_project(project_description: str, student_submission: str):

    prompt = f"""
You are an AI evaluator for SkillBridge AI.

Evaluate the student's project submission.

PROJECT DESCRIPTION:
{project_description}

STUDENT SUBMISSION:
{student_submission}

Evaluate:

1. Implementation quality
2. Project understanding
3. Strengths
4. Areas for improvement

Give scores from 0 to 10.

Return ONLY valid JSON in exactly this format:

{{
    "implementation_score": 0,
    "project_understanding_score": 0,
    "feedback": "Your detailed feedback here"
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    return json.loads(response.choices[0].message.content)