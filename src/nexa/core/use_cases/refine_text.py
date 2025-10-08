from ...interfaces.text_refiner import TextRefiner


class RefineText:
    def __init__(self, refiner: TextRefiner):
        self._refiner = refiner

    def execute(self, text: str) -> str:
        return self._refiner.refine(text)
