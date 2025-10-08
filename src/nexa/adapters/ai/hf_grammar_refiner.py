from typing import Any, Optional, cast

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

from ...interfaces.text_refiner import TextRefiner

_MODEL: Optional[T5ForConditionalGeneration] = None
_TOKENIZER: Optional[T5Tokenizer] = None


class HFGrammarRefiner(TextRefiner):
    def __init__(self, model_name: str = "UrukHan/t5-russian-spell"):
        global _MODEL, _TOKENIZER
        if _MODEL is None:
            _MODEL = T5ForConditionalGeneration.from_pretrained(model_name).to("cpu")
            _TOKENIZER = T5Tokenizer.from_pretrained(model_name, legacy=True)
        self.model = _MODEL
        self.tokenizer = _TOKENIZER

    def refine(self, text: str) -> str:
        print(f"[DEBUG] Input: {text!r}")
        if not text or not text.strip():
            return text
        input_text = f"grammar: {text.strip()}"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_length=128,
                num_beams=3,
                early_stopping=True,
                repetition_penalty=2.5,
                length_penalty=1.0,
            )
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"[DEBUG] Output: {result!r}")
        return cast(str, result).strip()
