def build_prompt(user_input: str) -> str:
    return f"""
Extract structured data from the following text.

Rules:
- action must be ONE of: call, meeting, email, task
- person = name or null
- time = ISO format or null

Return ONLY valid JSON. No markdown, no explanation.

Format:
{{
  "action": "",
  "person": null,
  "time": null
}}

Text:
{user_input}
"""
