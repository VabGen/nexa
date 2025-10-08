from typing import Optional, cast
import threading
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from ...interfaces.text_refiner import TextRefiner

# Глобальный кэш — загружаем модель один раз
_MODEL: Optional[T5ForConditionalGeneration] = None
_TOKENIZER: Optional[T5Tokenizer] = None
_INIT_LOCK = threading.Lock()


class HFGrammarRefiner(TextRefiner):
    def __init__(self, model_name: str = "UrukHan/t5-russian-spell"):
        global _MODEL, _TOKENIZER
        if _MODEL is None:
            with _INIT_LOCK:
                if _MODEL is None:
                    # Указываем CPU явно
                    device = torch.device("cpu")
                    # Ограничиваем число потоков (чтобы не грузить систему в FastAPI)
                    torch.set_num_threads(4)

                    _MODEL = T5ForConditionalGeneration.from_pretrained(
                        model_name,
                        torch_dtype=torch.float32,
                        low_cpu_mem_usage=True,
                    ).to(device)
                    _TOKENIZER = T5Tokenizer.from_pretrained(model_name, legacy=False)
        self.model = _MODEL
        self.tokenizer = _TOKENIZER
        self.device = torch.device("cpu")

    def refine(self, text: str) -> str:
        if not text or not text.strip():
            return text

        try:
            # Формирование входного текста
            task_prefix = f"Spell correct: {text.strip()}"

            # Токенизация (на CPU)
            inputs = self.tokenizer(
                task_prefix ,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=256,
            ).to(self.device)

            # Генерация без градиентов
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=128,
                    num_beams=4,
                    early_stopping=True,
                    repetition_penalty=1.2,
                    length_penalty=0.8,
                )

            # Декодирование
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return cast(str, result).strip()

        except Exception as e:
            print(f"[HFGrammarRefiner] Error refining text: {e}")
            return text
