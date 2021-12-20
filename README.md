# omoide-index

[![Build Status](https://github.com/IgorZyktin/omoide-index/workflows/test/badge.svg?branch=master&event=push)](https://github.com/IgorZyktin/omoide-index/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/IgorZyktin/omoide-index/branch/master/graph/badge.svg)](https://codecov.io/gh/IgorZyktin/omoide-index)
[![Python Version](https://img.shields.io/pypi/pyversions/omoide-index.svg)](https://pypi.org/project/omoide-index/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Сервер поисковой машины для проекта [Omoide](https://omoide.ru).

## Что делает

Принимает запросы по HTTP, ищет записи по заданным тегам. Позволяет применять
логические операции с тегами, например "кошки + собаки".

## Установка и запуск

TODO - Описать как запускать контейнер.

Используемые переменные окружения:

- **OMOIDE_INDEX_DATABASE_URI** - ссылка для подключения к базе данных.
- **OMOIDE_INDEX_RELOAD_ON_START** - включает и выключает автоматическую сборку
  индекса при первом запуске.

## Как работает

Команда запускает веб-сервер, хранящий в себе поисковый индекс. Он доступен
только для чтения, единственная доступная изменяющая операция - полная
перезагрузка индекса.

Сам индекс хранится в памяти в единственном экземпляре, поэтому сервис не может
масштабироваться горизонтально. Текущая реализация подразумевает только
вертикальное масштабирование, сопряжённое с покупкой более производительного
железа. В основном, опасения вызывает расход памяти и риск сожрать её всю. Но
предполагается, что проект не разрастётся настолько, что будет невозможно за
адекватные деньги подобрать железо для его запуска. Опасения именно про память,
потенциально индекс можно было бы запустить в нескольких экземплярах для
обработки большего числа запросов, но он и так достаточно быстр и это в общем
то не требуется.

По сути, вся история с этим индексом и сервером - моё желание проверить,
насколько много данных можно засунуть в питоновский словарик, а также то,
сможет ли он заменить базу данных. Сама идея изначально казалось глупой, но
быстродействие и простота реализации говорят об обратном.

## Интерфейс сервера

### Проверить работоспособность

Просто позволяет понять, что сервис вообще живой.

Пример запроса:

```shell
curl http://127.0.0.1:9000/
```

Пример ответа:

```shell
omoide-index 2021.12.20
```

### Проверить текущее состояние сервера

Предназначено для вызова человеком для проверки состояния сервиса. В первую
очередь - проверки расхода памяти.

Пример запроса:

```shell
curl http://127.0.0.1:9000/status
```

В ответ вернётся JSON объект с набором параметров.

| Имя поля         | Пример значения | Смысл поля             |
|-----------------:|-----------------|------------------------|
| version          | 2021.12.20      | Текущая версия сервера |
| server_restart   | 2021-10-05 20:15:21.050520+00:00 | Время последней перезагрузки сервера |
| server_uptime    | 15s             | Сколько времени прошло с последней перезагрузки сервера |
| server_memory    | 99.6 MiB        | Расход памяти на весь процесс сервера  |
| index_status     | active          | Текущее состояние сервера (init, active, reloading, fail) |
| index_reload     | 2021-10-05 20:15:24.813976+00:00 | Время последней перезагрузки индекса |
| index_uptime     | 11s             | Сколько времени прошло с последней перезагрузки индекса |
| index_duration   | 3.74            | Сколько секунд было потрачено на перезагрузку индекса |
| index_traceback  |                 | Текстовое описание сбоев при перезагрузке (пустая строка если всё нормально) |
| index_records    | 19733           | Общее число записей в индексе |
| index_buckets    | 20289           | Число "ячеек" индекса. Ячейка это набор uuid для одного тега |
| index_avg_bucket | 0.97            | Среднее число записей на один тег |
| index_min_bucket | 1               | Минимальное число записей на один тег |
| index_max_bucket | 17846           | Максимальное число записей на один тег |
| index_memory     | 46.8 MiB        | Расход памяти на объект индекса |
| registered_users | 4               | Общее число пользователей, для которых есть данные в индексе |

### Перезагрузить индекс

Предназначено для ручного вызова, после обновления базы данных. Позволяет мягко
перезагрузить содержимое индекса без перезагрузки самого сервера. Без этого
функционала при перезагрузке даунтайм сервера может достигать нескольких
минут (и чем больше будет расти индекс, тем дольше это будет работать). А при
работе через инструменты вроде gunicorn - достаточно долго, чтобы мастер
процесс посчитал, будто воркер уже умер. Фактически без специальных настроек
gunicorn вообще не может запустить сервер начиная с некоторого размера индекса.

Пример запроса:

```shell
curl -X POST http://127.0.0.1:9000/reload
```

Пример ответа:

```
reloading
```

Возвращает ответ мгновенно. Само задание исполняется в фоне. Факт окончания
можно узнавать делая запрос `/status`. Операция будет закончена, когда статус
перейдёт из `reloading` в `active` или `failed`.

Также эта операция запускается на старте сервера, чтобы заполнить индекс
данными для работы. В этом случае о готовности говорит переход из
статуса `init` в `active`. Переменно окружения **OMOIDE_INDEX_RELOAD_ON_START**
можно изменять это поведение. Значение `1` говорит о том, что обновление на
старте включено, а `0` что выключено.

Если при перезагрузке индекса что-то пошло не так, статус изменится на
`failed`. Работоспособность при этом не пострадает, старый индекс останется
актуальным.

### Выполнить поиск по тегам

Главная операция, ради которой сервер вообще существует. Предполагается, что он
очень быстро произведёт поиск по индексу и вернёт соответствующие записи.

Пример запроса:

```shell
curl -H "Content-Type: application/json" http://127.0.0.1:9000/search -d '...'
```

Предполагаемое тело запроса:

```json
{
    "user_uuid": "e1e977fa-b58b-458a-85e9-0a65df46aef4",
    "and": [
        "movie"
    ],
    "or": [
        "matrix"
    ],
    "not": [
        "matrix 4"
    ],
    "implicit_and": [
        "33428e50-efbd-4de5-acb8-367ce4aff72e"
    ],
    "implicit_or": [
    ],
    "implicit_not": [
        "2921c6a0-ebdb-438f-becb-9ab4165b3942"
    ],
    "page": 1,
    "items_per_page": 10
}
```

Поле user_uuid говорит о том, для кого делается запрос. Вернутся только
результаты, на которые у пользователя есть права.

Блоки and/or/not это списки тегов, требующие соответствующей логической
операции. Блоки implicit_and/implicit_or/implicit_not работают аналогично, но в
них находятся скрытые от пользователя технические теги (например uuid записей,
которые пользователь предпочёл сделать невидимыми в настройках).

Параметр items_per_page показывает на сколько страниц нарезать результат, а
параметр page показывает какую страницу из получившейся нарезки вернуть.

Пример ответа, когда сервер ещё не собрал индекс при первом запуске:

```json
{
    "items": [],
    "report": [],
    "time": 0.00001,
    "page": 0,
    "total_pages": 0,
    "total_items": 0,
    "announce": "Please wait a few minutes for server init after reload"
}
```

Пример полноценного ответа:

```json
{
    "items": [
        "010a6971-1209-46ef-b6f4-07546d676de4",
        "014e07f9-7119-4fd1-95e0-391e78c315a7",
        "01c1fd44-7f5a-4e03-bedf-6639b647a930",
        "01fd7287-4db1-4c2d-a3d6-01995349e32f",
        "03a26e29-3273-4766-8885-1fc3584d240e",
        "04137754-90cc-404e-9b8f-928f1ab27889",
        "0479f19c-9105-40aa-b5da-92d36cfe8f7e",
        "04a6e92c-ab26-4925-aeff-89d81ab6cf38",
        "05678e0d-0dec-4416-a621-35120ab41dac",
        "059605e5-2494-4f45-bb8a-c23608b0f95f"
    ],
    "report": [
        {
            "key": "start",
            "total": "33 429"
        },
        {
            "key": "found",
            "total": "486",
            "tag": "matrix",
            "sec": "0.00004"
        },
        {
            "key": "filter",
            "total": "486",
            "op": "OR",
            "sec": "0.00019"
        },
        {
            "key": "found",
            "total": "2 596",
            "tag": "movie",
            "sec": "0.00006"
        },
        {
            "key": "filter",
            "total": "486",
            "op": "AND",
            "sec": "0.00007"
        },
        {
            "key": "complete",
            "what": "sorting",
            "sec": "0.00012"
        }
    ],
    "time": 0.00041,
    "page": 1,
    "total_pages": 49,
    "total_items": 486,
    "announce": ""
}
```

Предполагается, что блоки из секции report потом будут локализованы в
приложении. В поле `announce` могут быть текстовые примечания, которые стоит 
показать пользователю (например сообщение о том, что индекс прямо сейчас 
перезагружается).

## License

[MIT](https://github.com/IgorZyktin/omoide-index/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [2e71727d0e666fc42c17f29897b1a59191c06428](https://github.com/wemake-services/wemake-python-package/tree/2e71727d0e666fc42c17f29897b1a59191c06428). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/2e71727d0e666fc42c17f29897b1a59191c06428...master) since then.
