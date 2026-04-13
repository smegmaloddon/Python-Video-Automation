# imports 
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# user imports
from src.utils import Configuration, Temporary

# functions
def Run(
    data : dict
) -> None:
    
    model_name = "google/flan-t5-small"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    prompt = f"""
    You are an expert viral YouTube title creator.

    TASK:
    Convert the input into ONE highly engaging, clickbait YouTube title.

    IMPORTANT:
    The input is ONLY a loose idea. You MUST reinterpret, exaggerate, or creatively reframe it.
    Do NOT rewrite the input literally. Do NOT describe it directly.

    RULES:
    - Maximum 10 words
    - Must be a strong viral hook (curiosity, shock, mystery, absurdity)
    - MUST feel like a real YouTube thumbnail title
    - You are allowed (and encouraged) to change wording, context, and framing
    - DO NOT repeat input words or phrases directly
    - DO NOT mirror input structure or phrasing
    - Avoid keyword lists or fragments — it must read like a headline
    - Use ALL CAPS for only 1–3 important words maximum (not everything)

    STYLE TARGET:
    Think viral documentary / MrBeast / “you won’t believe this” energy.
    The output should be MORE interesting than the input idea.

    FORBIDDEN:
    - Keyword dumping (e.g. “floating bear river stick water”)
    - Literal rephrasing
    - Repeating the input sentence structure
    - “X of X” constructions unless extremely natural

    GOOD EXAMPLES:

    Input: dog playing in snow
    Output: THIS DOG DID SOMETHING NO ONE EXPECTED IN THE SNOW

    Input: cats sleeping weird positions
    Output: YOU WON’T BELIEVE HOW THESE CATS SLEEP

    Input: bear walking in forest
    Output: A STRANGE BEAR WAS SPOTTED ALONE IN THE FOREST

    NOW DO THIS:

    Input: {data}

    Output:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=True,
        temperature=0.9
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result

