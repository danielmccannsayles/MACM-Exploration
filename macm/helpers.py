def list_to_numbered_string(arr: list) -> str:
    """Turn a list into a numbered string"""
    return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(arr))


def conditions_objectives_to_string(
    conditions: list, objectives: list
) -> tuple[str, str]:
    """This is done so many times I just made it a function"""
    return list_to_numbered_string(conditions), list_to_numbered_string(objectives)
