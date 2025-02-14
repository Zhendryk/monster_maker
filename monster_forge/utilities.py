from collections.abc import Sequence


def yes_or_no_question(
    prompt: str,
    yes_answers: Sequence[str] = ["yes", "y", "1"],
    no_answers: Sequence[str] = ["no", "n", "0"],
) -> bool:
    while True:
        prompt = f"{prompt}: "
        answer = input(prompt).lower().strip()
        if answer in yes_answers:
            return True
        elif answer in no_answers:
            return False
        else:
            print(
                f"Incalid answer: {answer}.\nPlease provide one of the following for yes: {yes_answers}\n Or one of the following for no: {no_answers}"
            )
            continue


def numbered_choice(
    options: Sequence[str],
    prompt: str = "Please select one of the following options by typing in its corresponding number",
) -> str:
    prompt = f"{prompt}:"
    for i, option in enumerate(options, start=1):
        prompt += f"\n\t{i}. {option}"
    prompt += "\n"
    answer_idx = None
    while True:
        answer = input(prompt)
        try:
            answer_idx = int(answer) - 1
            if answer_idx < 0 or answer_idx > len(options) + 1:
                print(
                    f"Invalid answer {answer}. Please select an option between 1 and {len(options) + 1}."
                )
                continue
            else:
                break
        except Exception as e:
            print(
                f"Invalid answer {answer}. Please select an option between 1 and {len(options) + 1}."
            )
            continue
    return options[answer_idx]
