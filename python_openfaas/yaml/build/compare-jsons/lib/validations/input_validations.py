

# helper method
def all_keys_exists(dict_to_validate, key_list):
    '''
    Validate that all keys in key_list exists in the dict_to_validate
    returned value:
        Two arguments tuple:
            arg1: boolean flag containing the validation status
                  True means valid and False mean not valid
            arg2: Missing keys list (in case any are missing)
    '''
    error_list = []
    is_valid = True
    dict_keys = dict_to_validate.keys()

    for input_key in key_list:
        if input_key not in dict_keys:
            error_list.append(input_key)

    if len(error_list) > 0:
        is_valid = False

    return is_valid, error_list
