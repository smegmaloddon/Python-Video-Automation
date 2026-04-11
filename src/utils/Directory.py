# imports
from pathlib import Path
import shutil

# cleanse folder of all sub-files & sub-directories
def Cleanse(
    folder : Path
) -> None:
    
    # verify 'folder' was provided & is not defaulted to None
    # verify 'folder' datatype is Path
    assert folder is not None and isinstance(
        folder, Path
    )

    # attempt to delete all files & folders using .iterdir()
    try:

        for file in folder.iterdir():

            # decide on action, depending on if file is folder or file
            match file.is_dir():

                case True:

                    # file is 'folder'
                    shutil.rmtree(
                        path=file
                    )
                
                case False:

                    # file is 'file'
                    file.unlink()

                case _:

                    # except
                    pass
    
    # found Exception with error & raise
    except Exception as error:

        raise Exception(
            error
        )

# replace old file with selected new file
def Replace(
    old : Path = None,
    new : Path = None
) -> None:
    
    # verify 'old' & 'new' are not None
    assert old is not None and new is not None, 'Path/s are \'None\''

    # assert that both Paths exist
    assert old.exists() and new.exists(), 'Path/s do not exist'

    # delete old file
    old.unlink()

    # replace with selected file
    new.replace(
        target=old
    )

    


