# imports
import yake

# functions
def Keywords(
    text : str = None
) -> list[str]:
    
    # verify 'text' is a string & not None
    assert text is not None and isinstance(
        text, str
    ), 'Parameters do not meet the correct requirements'

    # init model
    model : yake.KeywordExtractor = yake.KeywordExtractor()

    # extract keywords from text
    keywords : list[tuple] = model.extract_keywords(
        text=text
    )

    # format & save to array
    array : list = [
        keyword[0] for keyword in keywords
    ]

    return array