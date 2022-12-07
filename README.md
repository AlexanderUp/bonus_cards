# Веб-приложение для управления базой данных бонусных карт.

### Список моделей в БД
- Модель серии бонусных карт со следующими полями:
    - срок действия карт в серии;
    - дата выпуска карт в серии;
    - дата окончания активности карт в серии;
    - описание серии.
- Модель бонусной карты со следующими полями:
    - серия карты;
    - номер карты;
    - дата последнего использования карты;
    - баланс карты;
    - статус карты (не активирована/активирована/просрочена).

- Модель транзакции со следующими полями:
    - карта, с которой связана транзакция;
    - сумма транзакции;
    - дата транзакции;
    - описание транзакции.

### Функционал приложения:
- Генерация карт, с указанием серии и количества генерируемых карт;
- Просмотр списка карт с подробными данными;
- Поиск карт по заданным критериям;
- Просмотр профиля карты с историей покупок по ней;
- Активация/деактивация карты;
- Удаление карты.

### Описание процесса генерации карт:
- При необходимости создать новую серию карт с необходимым сроком действия;
- Генерировать необходимое количество карт, указав серию карт из шага 1.


### Существующие ограничения:
- Не смотря на реализацию модели транзакций на данном этапе отсутствует пересчет баланса карты (необходимо уточнение требований к процессу выпуска карты и расчета ее баланса);
- Все карты в одной серии имеют одинаковый срок выпуска и годности.

## Запуск приложения:
- Клонирование репозитория:

```https://github.com/AlexanderUp/bonus_cards.git```

- Переход в корневую папку проекта:

```cd bonus_cards```

- Создание виртуального окружения:

```python -m venv venv```

- Активация виртуального окружения (macOS):

```source venv/bin/activate```

- Переход в папку 'bonus':

```cd bonus```

- Создание и применение миграций:

```python manage.py makemigrations```
```python manage.py migrate```

- Создание суперпользователя (для доступа в административную часть приложения):

```python manage.py createsuperuser```

- Запуск сервера:

```python manage.py runserver```
