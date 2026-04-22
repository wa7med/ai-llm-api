from pydantic import BaseModel
from typing import Optional, Literal
import logging

logging.basicConfig(level=logging.INFO)


class InputRequest(BaseModel):
    input: str


class OutputResponse(BaseModel):
    action: Literal["call", "meeting", "email", "task"]
    person: Optional[str] = None
    time: Optional[str] = None


def log_request(input_text: str, output: dict):
    logging.info(f"INPUT: {input_text}")
    logging.info(f"OUTPUT: {output}")
