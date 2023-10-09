
def read_keywords_from_file():
    """
    Read and retrieve a list of searched keywords from a file.

    Opens and reads the 'searched_keywords.txt' file, splitting its content into a list of keywords.
    
    Returns:
    - A list of searched keywords obtained from the 'searched_keywords.txt' file.
    """
    with open('searched_keywords.txt', 'r') as file:
        keywords = file.read().splitlines()
    return keywords


def write_keyword_to_file(keyword):
    """
    Write a new keyword to the 'searched_keywords.txt' file if it is not already present.

    Appends the provided keyword to the 'searched_keywords.txt' file only if it is not
    already in the list of searched keywords.

    Args:
    - keyword (str): The keyword to be written to the file.

    """
      
    with open('searched_keywords.txt', 'a') as file:
        keywords = read_keywords_from_file()
        if keyword not in keywords:
            file.write(keyword + "\n")