import os

BASE_CACHE = os.path.abspath("./hf_cache")
os.makedirs(BASE_CACHE, exist_ok=True)

os.environ["HF_HOME"] = BASE_CACHE
os.environ["HUGGINGFACE_HUB_CACHE"] = BASE_CACHE
os.environ["TRANSFORMERS_CACHE"] = BASE_CACHE
os.environ["HF_HUB_CACHE"] = BASE_CACHE

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM
)


class LLMService:
    _generator = None

    @classmethod
    def get_generator(cls):
        if cls._generator is None:
            tokenizer = AutoTokenizer.from_pretrained(
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                cache_dir=BASE_CACHE
            )

            model = AutoModelForCausalLM.from_pretrained(
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                cache_dir=BASE_CACHE
            )

            cls._generator = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer
            )

        return cls._generator

    @classmethod
    def generate_response(cls, prompt):
        generator = cls.get_generator()

        result = generator(
            prompt,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True
        )

        generated_text = result[0]["generated_text"]

        if "Assistant:" in generated_text:
            reply = generated_text.split("Assistant:")[-1].strip()
        else:
            reply = generated_text.strip()

        return reply
