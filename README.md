# DE course of ITMO university
**Student: Мухтаров Тимерлан Тахирович**

Описание проекта: 
Область проекта: Недвижимость
Бизнес-проблема: Определение факторов, влияющих на цену квартир в Москве

В условиях динамично развивающегося рынка недвижимости в Москве, одной из ключевых задач для агентств, застройщиков и покупателей является точная оценка стоимости квартир. Существует множество факторов, которые могут влиять на цену недвижимости, такие как расположение, площадь, этажность, год постройки, наличие ремонта и другие.

Однако, на практике, оценка цен зачастую бывает субъективной и зависит от множества переменных, которые трудно учесть без систематического подхода. В связи с этим, целью данного проекта является сбор данных о недвижимости в Москве с целью выявления закономерностей и факторов, которые оказывают наибольшее влияние на цену квартиры.

Структура проекта:
  DE_HM/  
├── data/  
│   ├── raw/  
│   └── preprocessed/  
├── db/  
│   └── apartments.db  
├── src/  
│   ├── data_collection.py  
│   ├── data_preprocessing.py  
│   ├── preprocessing.ipynb  
│   └── data_storage.py  
├── dashboard.py  
├── pipeline.py  
└── requirements.txt  



## 1. Сбор данных (data_collection.py)
Для сбора данных использовался открытый датасет из Kaggle, а также были предприняты попытки парсинга с **Cian**.
Для парсинга были использованы следующие инструменты:
- **Requests**: Для отправки HTTP-запросов на страницы сайта и получения данных.
- **BeautifulSoup**: Для парсинга HTML-кода страниц и извлечения нужной информации.
- **UserAgent**: Для имитации реального пользователя.

*Файл для сбора данных*: [data_collection.py](./src/data_collection.py)

## 2. Очистка и предобработка данных (data_preprocessing.py & preprocessing.ipynb)
**Инструменты**: pandas

После получения данных они были очищены и подготовлены для дальнейшего анализа. Это включало несколько ключевых шагов:
- **Удаление дубликатов**: Проверка и удаление строк с одинаковыми квартирами (по ссылкам на объявления).
- **Обработка выбросов**: Удаление аномально высоких и низких цен на квартиры (в связи с ошибками заполнения/реальными выбросами).
- **Приведение данных к нужному типу**: Некоторые данные, такие как цены или площади, изначально могли быть строками, и их нужно было преобразовать в числовые значения.

В задании также указано провести стандартизацию или нормализацию, а также обработать пропущенные значения, но перед разбиением на train/test/val этого лучше не делать во избежании утечки данных.

*Файл для предобработки данных*: [data_preprocessing.py](./src/data_preprocessing.py)

*Jupyter notebook для анализа данных*: [preprocessing.ipynb](./src/preprocessing.ipynb)

## 2.1. Исследовательский анализ данных (EDA) (preprocessing.ipynb)
**Инструменты**: pandas, seaborn, matplotlib

В рамках пункта 2 также был проведен **EDA** (Exploratory Data Analysis), чтобы понять, как различные характеристики недвижимости влияют на цену. Для этого использовались визуализации и статистические методы:
- **Бокс-плоты**: Для визуализации распределения числовых признаков, таких как цена, площадь, этажность и т.д. Это позволило выявить выбросы и понять, как значения распределяются.
- **Гистограммы**: Для оценки распределения цен на квартиры.
- **Тепловая карта корреляций**: Для изучения взаимосвязей между различными числовыми признаками, чтобы понять, какие факторы наиболее сильно влияют на цену.
- **Графики рассеяния**: Для изучения зависимостей между ценой и другими характеристиками, такими как этаж, площадь и т.д.

*Пример анализа данных*: см. [preprocessing.ipynb](./src/preprocessing.ipynb)

## 3. Визуализация на дашборде (dashboard.py)
**Инструменты**: streamlit, pandas, seaborn, matplotlib

Для представления данных и результатов анализа был создан интерактивный дашборд с использованием **Streamlit**. Он включает в себя графики, полученные на этапе **EDA**, и позволяет итеративно выбирать нужные для отображения признаки.

*Файл для дашборда*: [dashboard.py](./dashboard.py)

## 4. Сохранение данных в хранилище данных (data_storage.py)
**Инструменты**: sqlalchemy, sqlite

Реляционная база данных **sqlite** подходит для хранения табличных данных о квартирах. В этом файле происходит сохранение и загрузка данных из базы.

*Файл для работы с базой данных*: [data_storage.py](./src/data_storage.py)

## 5. Работа с программой (pipeline.py)
**Инструменты**: prefect

Для организации пайплайна работы проекта был использован **Prefect** — легкий и простой аналог **Airflow**, который помогает автоматизировать процессы в проекте, такие как сбор, обработка и хранение данных.

*Файл для пайплайна*: [pipeline.py](./pipeline.py)

---

Для запуска кода и работы с проектом из корневого каталога проекта.

python pipeline.py - пайплайн работы с данными

streamlit run dashboard.py - дашборд
