# imports
from concurrent.futures import ThreadPoolExecutor

# functions
def Thread(
    func : object = None,
    items : list[dict] = [], # [ {_key1 = _value1}, {_key2 = _value2} ]
    workers : int = 4
) -> None:
    
    # thread downloads for speed
    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:
        
        # create futures list
        futures : list = [
            executor.submit(
                func, **item
            )
            for item in items
        ]

        # wait
        for future in futures:

            future.result()