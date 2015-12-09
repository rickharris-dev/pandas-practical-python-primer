friends = [
    {
        "id": "BFP",
        "first_name": "Big Fat",
        "last_name": "Panda",
        "telephone": "574-NOO-DLES",
        "email": "mike@eikonomega.com",
        "notes": "My bestest friend in all the world."
    },
    {
        "id": "VinDi",
        "first_name": "Vin",
        "last_name": "Diesel",
        "telephone": "I-HIT-PEOPLE",
        "email": "vdiesel4@supercool.edu",
        "notes": "Really annoying guy. Will never amount to anything."
    }
]

def existing_friend(id:str) -> dict:
    """
    Return a representation of friend resource that matches a given
    'id' if it exits.

    Args:
        id (str): The id value to search for a resource with.

    Returns:
        A dictionary representation of the friend resource or None if
        no match is found.
    """
    for friend in friends:
        if id.lower() == friend['id'].lower():
            return friend