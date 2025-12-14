#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pipeline_sum_series import SeriesPipeline

if __name__ == "__main__":
    pipeline = SeriesPipeline(x=1.2)
    print(pipeline)

    pipeline.run()

    print("\n--- Итог ---")
    print(f"Сумма ряда     = {pipeline.series_result}")
    print(f"Аналитическое  = {pipeline.final_result}")

    if pipeline.series_result is not None and pipeline.final_result is not None:
        error = pipeline.series_result - pipeline.final_result
        print(f"Абсолютная погрешность   = {error}")
