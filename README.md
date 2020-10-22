# Battle city
[![Build Status](https://travis-ci.com/marcenavuc/battle_city.svg?branch=main)](https://travis-ci.com/marcenavuc/battle_city)
[![codecov](https://codecov.io/gh/marcenavuc/battle_city/branch/main/graph/badge.svg?token=CqWsSCNbTx)](undefined)

Автор: Аверченко Марк (https://vk.com/markenus)

## Описание
Простая имплементация battle city на python 

## Требования
* Python версии ровно 3.6
* Все библиотеки из файла requirements.txt

## Установка
1) Скачайте репозиторий
`git clone marcenavuc/battle_city`
2) Установите зависимости
`pip install -r requirements.txt`

## Установить как пакет
1) Установите setuptools, wheel
```bash
$ python3 -m pip install setuptools wheel
```
2) Соберите исходный код для установки
```bash
$ python3 setup.py sdist bdist_wheel
```
3) Соберите исходники и установите пакет
```bash
$ python3 setup.py build
$ python3 setup.py install
```

## Состав
* Настройки: **battle_city/config.py**
* Имплементация уровня: **battle_city/level.py**
* Отображение игры: **battle_city/view.py**
* Медиа файлы: **battle_city/media**
* Игровые объекты: **battle_city/game_objects**
* Тесты: **tests/**

## Использование
`python __main__.py`
