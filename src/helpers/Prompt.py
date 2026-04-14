# imports 
import ollama

# user imports
from src.utils import Configuration, Temporary

# functions
def Run(
    text : str = None,
    model : str = 'llama3'
) -> None:
    
    # verify 'text'
    assert text is not None and isinstance(
        text, str
    )
   
    # fetch response
    response : ollama.ChatResponse = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'User',
                'content': text
            }
        ]
    )

    return response['message']['content']

