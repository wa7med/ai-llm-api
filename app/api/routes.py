from fastapi import APIRouter
from app.schemas.request_response import InputRequest, log_request
from app.services.llm_service import call_llm
from app.utils.prompt_builder import build_prompt

router = APIRouter()


@router.post("/process")
def process_input(request: InputRequest):
    prompt = build_prompt(request.input)
    result = call_llm(prompt)
    log_request(request.input, result)
    return result
