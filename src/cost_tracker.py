INPUT_COST_PER_MILLION = 0.075
OUTPUT_COST_PER_MILLION = 0.30


def calculate_llm_cost(
    input_tokens: int,
    output_tokens: int,
) -> float:
    """
    Calculate the estimated LLM cost in USD.
    """

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_PER_MILLION

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_PER_MILLION

    return round(input_cost + output_cost, 6)