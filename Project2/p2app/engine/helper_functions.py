def remove_none_dict(dictionary: dict) -> dict:
    """Removes none values from a dictionary"""
    return {key: val for key, val in dictionary.items() if val is not None}
def create_where_from_dict(dictionary: dict) -> str:
    """Creates a where statement based off a dictionary"""
    where = []
    for key in dictionary.keys():
        string_key = f'{key} = :{key}'
        where.append(string_key)
    where = ' AND '.join(where)
    return where
def create_values_from_dict(dictionary: dict) -> str:
    """Creates a values statement based off a dictionary"""
    temp_keys = list(dictionary.keys())
    for index, val in enumerate(temp_keys):
        temp_keys[index] = f':{val}'
    values = ', '.join(temp_keys)
    return f'({values})'

def create_insert_from_dict(dictionary: dict) -> str:
    """Creates an insert statement based off a dictionary"""
    temp_keys = list(dictionary.keys())
    insert = ', '.join(temp_keys)
    return f'({insert})'
def create_set_from_dict(dictionary: dict) -> str:
    """Creates a set statement based off a dictionary"""
    set_list = []
    for key, val in dictionary.items():
        set_list.append(f'{key} = :{key}')
    set_str = ', '.join(set_list)
    return set_str

def get_new_unused_id(table_name: str, connection: 'Connection') -> int:
    """Gets an unused id number based off a provided table"""
    cursor = connection.execute(
        f'''SELECT {table_name}_id'''
        f''' FROM {table_name}'''
    )
    result = cursor.fetchall()
    cursor.close()
    ans = 0
    for res in result:
        ans += res[0]
    return ans + 1