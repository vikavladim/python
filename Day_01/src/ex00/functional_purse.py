def add_ingot(old: dict, amount=1):
    new_dict = old.copy()
    new_dict.setdefault('gold_ingots', 0)
    new_dict['gold_ingots'] += amount
    return new_dict


def get_ingot(old: dict, amount=1):
    if 'gold_ingots' not in old or old['gold_ingots'] < amount:
        return empty(old)

    new_dict = old.copy()
    new_dict['gold_ingots'] -= amount
    return new_dict


def empty(old: dict = None):
    if old:
        new_dict = old.copy()
        new_dict.pop('gold_ingots', None)
        return new_dict
    return {}


if __name__ == '__main__':
    purse = {'gold_ingots': 2, 'banana': 3}
    print('Start purse: ', purse)
    print('Add to purse with 2 gold_ingots: ', add_ingot(purse))
    print('Start purse: ', purse)
    print('Get from purse with 2 gold_ingots: ', get_ingot(purse))
    print('Start purse: ', purse)
    print('Add to empty purse: ', add_ingot(empty(purse)))
    print('Start purse: ', purse)
    print('Get from empty purse: ', get_ingot(empty(purse)))
    print('Start purse: ', purse)
    print('Example from readme: ', add_ingot(get_ingot(add_ingot(empty(purse)))))
    print('Start purse: ', purse)

    empty_purse = empty({'apple': 3})
    print('Empty purse: ', empty_purse)
    print('Get from empty purse: ', get_ingot(empty_purse))
    print('Add to empty purse: ', add_ingot(empty_purse))
