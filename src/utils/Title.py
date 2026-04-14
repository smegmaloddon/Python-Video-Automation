# imports 
import ollama

# user imports
from src.utils import Configuration, Temporary

# functions
def Run(
    data : dict
) -> None:
    
    # text prompt
    text = f'''
        You are an expert YouTube viral content strategist.

        Your job is to generate ONE highly clickable viral YouTube title based ONLY on the metadata provided.

        You will be given a dictionary containing signals such as:
        - keywords
        - video topic hints
        - duration
        - objects/subjects involved
        - context clues

        IMPORTANT RULES:
        - Do NOT repeat the keywords directly
        - You must INTERPRET the data, not copy it
        - Create curiosity, mystery, or shock
        - Make it feel like a viral YouTube Shorts title
        - Must be under 10 words
        - Must be ALL CAPS
        - Must sound natural and human, not robotic
        - Focus on storytelling implication, not literal description

        You must infer the most interesting possible scenario from the data.

        Return ONLY the title. No explanations.

        Metadata:
        {data}

        Output should only be the title, if it is not the title ONLY, the response is void
    '''
    
    # fetch response
    response : ollama.ChatResponse = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'User',
                'content': text
            }
        ]
    )

    return response['message']['content']

