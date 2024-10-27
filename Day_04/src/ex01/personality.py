import random
import time


def turrets_generator():
    while True:
        personality_traits = {
            'neuroticism': random.randint(0, 40),
            'openness': random.randint(0, 40),
            'conscientiousness': random.randint(0, 40),
            'extraversion': random.randint(0, 40),
            'agreeableness': 0
        }

        personality_traits['agreeableness'] = 100 - sum(personality_traits.values())
        if personality_traits['agreeableness'] < 0:
            continue

        turret = type('Turret', (), {
            'personality_traits': personality_traits,
            'actions': {
                'shoot': lambda: print('Shooting'),
                'search': lambda: print('Searching'),
                'talk': lambda: print('Talking'),
            }
        })

        yield turret()


if __name__ == '__main__':
    for turret in turrets_generator():
        print(turret.personality_traits)
        turret.actions['shoot']()
        turret.actions['search']()
        turret.actions['talk']()
        time.sleep(0.1)
