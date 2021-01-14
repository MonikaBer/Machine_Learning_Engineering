from enum import IntEnum

class User:

    def __init__(self, user):
        self.user_id = user['user_id']
        self.gender = get_gender_from_name(user['name'])
        self.city = user['city']


class Gender(IntEnum):
    MALE = 0
    FEMALE = 1
    UNKNOWN = 2

def get_gender_from_name(name):
    space_pos = name.find(' ')
    if space_pos == -1:
        return Gender.UNKNOWN

    first_name = name[:space_pos]
    #print("first name = {}".format(first_name))
    if first_name[len(first_name) - 1] == 'a' or first_name == 'Nicole':
        return Gender.FEMALE
    
    return Gender.MALE
