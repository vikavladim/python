# Содержание

- [Упражнение 00: Функциональный кошелек](#упражнение-00-функциональный-кошелек)
- [Упражнение 01: Разделение](#упражнение-01-разделение)
- [Упражнение 02: Охранная сигнализация](#упражнение-02-охранная-сигнализация)

# Упражнение 00: Функциональный кошелек

Необходимо реализовать функции `add_ingot(purse)`, `get_ingot(purse)` и `empty(purse)`, которые работают с кошельком (словарем типа `typing.Dict[str, int]`). Функции должны возвращать новый кошелек и не должны изменять переданный аргумент. Композиция `add_ingot(get_ingot(add_ingot(empty(purse)))` должна вернуть `{"gold_ingots": 1}`.

# Упражнение 01: Разделение

Функция `split_booty` должна принимать несколько кошельков и возвращать три кошелька таким образом, чтобы разница между количеством слитков в любых двух кошельках была не больше 1.

# Упражнение 02: Охранная сигнализация

Необходимо добавить новое поведение к функциям `add_ingot(purse)`, `get_ingot(purse)` и `empty(purse)`, чтобы при их вызове выводилось слово `SQUEAK`, не изменяя тело функций.