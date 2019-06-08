slack-bot-on-board
==================
Описание задач по проекту в Trello
------------------------------------

*Отправка по расписанию*
Используется библиотека https://pypi.org/project/schedule/
Ежедневно скрипт смотрит есть ли данные для отправки на данный день
Если нет, то он ждет следующего дня
Если есть отправляет заявленные данные заявленному пользователю

*База данных*
3 базы

Пользователи (исп в админке Flask):
ID пользователя
Имя
Должность (тип)
Дата начала работы

Материалы (исп в админке Flask):
ID события
Текст
Когда отправить относительно даты начала работы (+1/2/3 и тд дней)

Расписание (исп библиотеку schedule:
ID отправки
ID пользователя
ID события
Время для отправки (поле начало работы + поле когда отправить относительно)
Статус (отправлено или нет)