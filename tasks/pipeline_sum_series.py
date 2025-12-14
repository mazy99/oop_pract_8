#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from threading import Event, Thread


class SeriesPipeline:

    def __init__(self, x: float = 1.2, eps: float = 10**-7) -> None:

        self.x: float = x
        self.eps: float = eps

        self.series_result: float | None = None
        self.final_result: float | None = None

        self.ready_event: Event = Event()

    def _term(self, n: int) -> float:
        return ((-1) ** n) * (self.x**n) / (2 ** (n + 1))

    def _first_worker(self, index: int) -> None:
        print(f"[Thread {index}] Начало вычисления ряда")

        s: float = 0.0
        n: int = 0

        while True:
            a_n = self._term(n)
            if abs(a_n) < self.eps:
                break
            s += a_n
            n += 1

        self.series_result = s
        print(f"[Thread-1] Сумма ряда = {s}")
        self.ready_event.set()

    def _second_function(self) -> float:
        return 1 / (2 + self.x)

    def _second_worker(self, index: int) -> None:
        print(f"[Thread {index}] Ожидание результата первой функции")
        self.ready_event.wait()

        assert self.series_result is not None
        self.final_result = self._second_function()

        print(f"[Thread {index}] Результат второй функции = {self.final_result}")

    def run(self) -> None:
        t1: Thread = Thread(target=self._first_worker, args=(1,))
        t2: Thread = Thread(target=self._second_worker, args=(2,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def __str__(self) -> str:
        return (
            "Ряд:\n"
            "S = Σ [(-1)^n * x^n / 2^(n+1)], n = 0 .. ∞\n\n"
            f"x = {self.x}\n"
            f"epsilon = {self.eps}\n\n"
            "Аналитическое выражение:\n"
            "S = 1 / (2 + x)"
        )
