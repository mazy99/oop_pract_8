import pytest

from tasks.pipeline_sum_series import SeriesPipeline


def test_term_calculation() -> None:
    pipeline = SeriesPipeline(x=1.2)

    assert pipeline._term(0) == pytest.approx(1 / 2)

    assert pipeline._term(1) == pytest.approx(-1.2 / 4)

    assert pipeline._term(2) == pytest.approx((1.2**2) / 8)


def test_second_function() -> None:
    x = 1.2
    pipeline = SeriesPipeline(x=x)

    expected = 1 / (2 + x)
    assert pipeline._second_function() == pytest.approx(expected)


def test_series_convergence() -> None:
    pipeline = SeriesPipeline(x=1.2, eps=1e-7)

    pipeline.run()

    assert pipeline.series_result is not None

    expected = 1 / (2 + pipeline.x)

    assert pipeline.series_result == pytest.approx(expected, abs=1e-7)


def test_pipeline_final_result() -> None:
    pipeline = SeriesPipeline(x=0.5, eps=1e-7)

    pipeline.run()

    assert pipeline.series_result is not None
    assert pipeline.final_result is not None

    expected = 1 / (2 + 0.5)

    assert pipeline.final_result == pytest.approx(expected)


def test_event_is_set() -> None:
    pipeline = SeriesPipeline()

    pipeline.run()

    assert pipeline.ready_event.is_set()


@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 1.5])
def test_series_for_different_x(x: float) -> None:
    pipeline = SeriesPipeline(x=x, eps=1e-7)

    pipeline.run()

    expected = 1 / (2 + x)

    assert pipeline.series_result == pytest.approx(expected, abs=1e-7)
    assert pipeline.final_result == pytest.approx(expected)
