# Содержание

- [Упражнение 00: Энергетический Поток](#упражнение-00-энергетический-поток)
- [Упражнение 01: Личности](#упражнение-01-личности)
- [Упражнение 02: Противодавление](#упражнение-02-противодавление)

# Упражнение 00: Энергетический Поток

### Задача: написать скрипт `energy.py` с функцией `fix_wiring()`

#### Описание функции

Функция `fix_wiring()` должна принимать три итерируемых объекта: `cables`, `sockets` и `plugs`. Она должна вернуть
другой итерируемый объект, содержащий строки с командами для подключения кабелей к розеткам.

#### Требования

* Функция не должна делать предположений о длине входных итерируемых объектов.
* Если нет достаточно кабелей или розеток, они не должны присутствовать в выходном итерируемом объекте.
* Входные итерируемые объекты могут содержать не только строки, которые должны быть отфильтрованы.
* Вы можете получить дополнительные баллы, если тело вашей функции может быть написано только с использованием одной
  строки (начинающейся с return)

#### Примеры

```python
plugs = ['plug1', 'plug2', 'plug3']
sockets = ['socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable1', 'cable2', 'cable3', 'cable4']

for c in fix_wiring(cables, sockets, plugs):
    print(c)
```

**Вывод**

```
plug cable1 into socket1 using plug1
plug cable2 into socket2 using plug2
plug cable3 into socket3 using plug3
weld cable4 to socket4 without plug
```

#### Дополнительный пример:

```python
plugs = ['plugZ', None, 'plugY', 'plugX']
sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
cables = ['cable2', 'cable1', False]
```

**Вывод**

```
plug cable2 into socket1 using plugZ
plug cable1 into socket2 using plugY
```

# Упражнение 01: Личности

#### Требования

* Создать генераторную функцию `turrets_generator()` в файле `personality.py`
* Функция должна генерировать класс `Turret` и его экземпляры динамически без использования ключевого слова `class`
* Класс `Turret` должен иметь три метода: `shoot`, `search` и `talk`, которые выводят на экран соответствующие сообщения
* Каждый экземпляр класса `Turret` должен иметь пять личностных черт: `neuroticism`, `openness`, `conscientiousness`,
  `extraversion` и `agreeableness`, которые являются случайными числами от 0 до 100
* Сумма всех пяти личностных черт для каждого экземпляра должна быть равна 100

# Упражнение 02: Противодавление

Создать файл `pressure.py` с генераторной функцией `emit_gel()`, которая имитирует измеренное давление жидкости. Функция
должна генерировать бесконечный поток чисел от 50 до 100 (значения > 100 считаются ошибкой) с случайным шагом,
отобранным из диапазона `[0, step]`, где `step` является аргументом генератора `emit_gel()`.

* Рабочее давление должно быть между 20 и 80.
* Если генератор в какой-то момент выдает значение ниже 20 или выше 80, должна быть применена операция, которая изменит
  знак шага.
* Если давление выше 90 или ниже 10, генератор `emit_gel()` должен быть закрыт и скрипт должен завершиться.

Для контроля давления нужно написать другую функцию с именем valve(), которая будет перебирать значения emit_gel() и
использовать .send() метод для изменения знака текущего шага.