from ex00.functional_purse import *


# def split_booty(*kwargs):
#     if len(kwargs) == 0:
#         return {}
#     count = 0
#     k = [a.copy() for a in kwargs]
#     for i in k:
#         count += i.get('gold_ingots', 0)
#     # avg = count // len(k)
#     avg = count // 3
#     for i in k:
#         i['gold_ingots'] = avg
#     for i in range(count % len(k)):
#         k[i]['gold_ingots'] += 1
#     return tuple(k)


def split_booty(*kwargs):
    # if len(kwargs) == 0:
    #     return {}
    count = 0
    purses = [a.copy() for a in kwargs]
    result = [empty() for _ in range(3)]
    for i in purses:
        count += i.get('gold_ingots', 0)
    # avg = count // len(k)
    avg = count // 3
    for i in result:
        i['gold_ingots'] = avg
    for i in range(count % 3):
        result[i]['gold_ingots'] += 1
    return tuple(result)


if __name__ == '__main__':
    print(split_booty({'gold_ingots': 2}, {}, {'gold_ingots': 5, 'apple': 3}))
    print(split_booty())

