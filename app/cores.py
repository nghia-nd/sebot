from warnings import warn

from transformers import AutoModelForCausalLM, AutoTokenizer

from .configs import GenerationConfig, generation_config, llm_config
from .warnings import PromptTruncationWarning

_tokenizer = AutoTokenizer.from_pretrained(
    llm_config.root_path, **llm_config.tokenizer_kwargs
)
_model = AutoModelForCausalLM.from_pretrained(
    llm_config.root_path, **llm_config.transformer_kwargs
)


def generate_response(prompt: str, config: GenerationConfig = generation_config) -> str:
    max_length = _tokenizer.model_max_length

    input_ids = _tokenizer(prompt, return_tensors='pt').input_ids

    if input_ids.shape[1] > max_length:
        input_ids = input_ids[:, :max_length]
        warn(
            f'Truncated to a maximum of {max_length}.',
            PromptTruncationWarning,
        )

    output_embeddings = _model.generate(
        input_ids, **config.model_dump(), return_dict_in_generate=False
    )

    response_only_embedding = output_embeddings.squeeze()[input_ids.shape[1] :]
    return _tokenizer.decode(response_only_embedding, skip_special_tokens=True)
