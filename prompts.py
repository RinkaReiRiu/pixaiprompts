from pathlib import Path

PROMPT_DIR = Path("prompts")

def load(name):
    with open(
        PROMPT_DIR / name,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()

system_promptsAnalizer = load(
    "prompts_analyzer.txt"
)

system_promptsImplementer = load(
    "prompts_implementer.txt"
)

system_analizer = load(
    "analyzer.txt"
)

system_implementer = load(
    "implementer.txt"
)

system_evaluator = load(
    "evaluator.txt"
)

system_reimplementer = load(
    "reimplementer.txt"
)