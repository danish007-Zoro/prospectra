from src.cost_tracker import calculate_llm_cost


def test_zero_tokens_have_zero_cost():
    assert calculate_llm_cost(0, 0) == 0.0


def test_input_token_cost():
    cost = calculate_llm_cost(
        input_tokens=1_000_000,
        output_tokens=0,
    )

    assert cost == 0.075


def test_output_token_cost():
    cost = calculate_llm_cost(
        input_tokens=0,
        output_tokens=1_000_000,
    )

    assert cost == 0.30


def test_combined_token_cost():
    cost = calculate_llm_cost(
        input_tokens=1_000_000,
        output_tokens=1_000_000,
    )

    assert cost == 0.375


def test_small_usage_is_calculated_correctly():
    cost = calculate_llm_cost(
        input_tokens=3_646,
        output_tokens=1_264,
    )

    assert cost == 0.000653