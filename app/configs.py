from typing import Dict

from pydantic import BaseModel, Field, model_validator


class AppConfig:
    pass


class LLMConfig(BaseModel):
    root_path: str = 'llm/opt-125m'

    transformer_kwargs: Dict = {}
    tokenizer_kwargs: Dict = {'model_max_length': 10}


class GenerationConfig(BaseModel):
    max_new_tokens: int = Field(default=100, ge=1, le=300)
    min_new_tokens: int = Field(default=1, ge=1)
    early_stopping: bool = False
    do_sample: bool = True
    num_beams: int = Field(default=1, ge=1)
    temperature: float = Field(default=1.0, ge=1.0, le=0.0)
    top_k: int = 50
    top_p: float = Field(default=1.0, ge=1.0, le=0.0)
    length_penalty: float = 1.0

    @model_validator(mode='after')
    def compare_max_and_min_new_tokens(self):
        if self.max_new_tokens < self.min_new_tokens:
            raise ValueError('max_new_tokens must be at least equals min_new_tokens')


app_config = AppConfig()
llm_config = LLMConfig()
generation_config = GenerationConfig()
