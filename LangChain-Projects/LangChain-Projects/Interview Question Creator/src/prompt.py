
prompt_template = """
You are an expert at creating questions based on the provided material and documentation.
Your goal is to prepare a student or professional for their exam or interview.
You do this by asking questions about the text below:

------------
{text}
------------

Create questions that will prepare the reader for tests or interviews.
Make sure not to lose any important information.

QUESTIONS:
"""



refine_template = ("""
You are an expert at creating practice questions based on the provided material.
Your goal is to help someone prepare for an exam or interview.

Here are the existing questions generated so far:
{existing_answer}

Below is additional context from the document:
------------
{text}
------------

Instructions:
- Add new questions that cover important topics NOT already addressed.
- Remove duplicate or overly similar questions.
- Ensure all questions are clear, specific, and test real understanding.
- Do NOT include questions answerable with a simple yes/no.
- Return the complete final list of questions.

QUESTIONS:
""")
