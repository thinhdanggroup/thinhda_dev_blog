# Import libraries
import os

import openai
import requests
from dotenv import load_dotenv

load_dotenv()

# Define constants
openai.api_key = os.environ["OPENAI_API_KEY"]

MAX_CANDIDATES = 5
MAX_STEPS = 5

# Define verdicts
verdicts = ["sure", "maybe", "impossible"]

# Define markdown template
md_template = """
# {personal_information}

## Education

{education}

## Work Experience

{work_experience}

## Projects

{projects}

## Skills

{skills}
"""


# Define ToT functions

# Generate candidates using CoT prompts
def generate_candidates():
    system_prompt = ("""You are writing a resume. Please write a paragraph follow format:
Personal information:
Education:
Work experience:
Projects:
Skills:""")

    message = """
Personal information: Thinh Dang
Education: Ho Chi Minh University of Technology
Work experience: Software Engineer at Trusting Social
Projects:
- Artificial General Intelligence (AGI) Researcher at Trusting Social
Skills: 
- Python 
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )

    print(response)
    output = response.choices[0].text
    candidates = output.split("\n\n")
    candidates = [c.strip() for c in candidates if c.strip()]
    candidates = candidates[:MAX_CANDIDATES]
    return candidates


# Evaluate candidates using verdicts
def evaluate_candidates(candidates):
    message = "Rate each candidate as sure/maybe/impossible with regard to reaching the final goal.\n"
    message += "\n".join([f"{i + 1}. {c}" for i, c in enumerate(candidates)])
    message += "\n\n"
    messages = [
        {"role": "user", "content": message},
    ]

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )

    output = response.choices[0].text
    ratings = output.split("\n")
    ratings = [r.strip() for r in ratings if r.strip()]
    ratings = ratings[:len(candidates)]
    return ratings


# Perform breadth-first search using ToT controller
def breadth_first_search(step, context):
    # Check termination condition
    if step == MAX_STEPS:
        return context
    # Generate candidates
    candidates = generate_candidates()
    # Evaluate candidates
    ratings = evaluate_candidates(candidates)
    # Loop over candidates
    for i in range(len(candidates)):
        # Check rating
        if ratings[i] == "sure":
            # Update context
            context[cot_prompts[step].split()[0][:-1]] = candidates[i]
            # Recurse to the next step
            result = breadth_first_search(step + 1, context)
            # Check result
            if result:
                return result
        elif ratings[i] == "maybe":
            # Update context
            context[cot_prompts[step].split()[0][:-1]] = candidates[i]
            # Recurse to the next step with a lower depth limit
            result = breadth_first_search(step + 1, context, depth - 1)
            # Check result
            if result:
                return result
        else:
            # Skip candidate
            continue
    # Return None if no solution found
    return None


# Display the final resume text using markdown
def display_resume(context):
    md = md_template.format(**context)
    print(md)


# Run ToT for resume writing task
context = {}
resume = breadth_first_search(0, context)
if resume:
    display_resume(resume)
else:
    print("No resume found.")
