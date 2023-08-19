from enum import Enum
from time import time
from warnings import catch_warnings, simplefilter

from pydantic import BaseModel

from app import api

from .configs import GenerationConfig, generation_config
from .cores import generate_response
from .warnings import PromptTruncationWarning


class GenerationWarning(str, Enum):
    PROMPT_TRUNCATION = 'prompt_truncation'


class ChatRequest(BaseModel):
    prompt: str
    config: GenerationConfig = generation_config
    # TODO: add task_type with pre-configured instructions


class ChatResponse(BaseModel):
    response: str
    warning: GenerationWarning | None
    elapsed_time: float


@api.post('/chats')
def create_chat(chat_request: ChatRequest):
    warning = None
    with catch_warnings(record=True) as msgs:
        simplefilter('always')
        start_time = time()
        response = generate_response(
            prompt=chat_request.prompt, config=chat_request.config
        )
        end_time = time()

        if [msg for msg in msgs if issubclass(msg.category, PromptTruncationWarning)]:
            warning = GenerationWarning.PROMPT_TRUNCATION.value

    return ChatResponse(
        response=response, warning=warning, elapsed_time=end_time - start_time
    )
