# InfoteksTestTask

#### Дополнительно: дать пример команды для настройки автоматического запуска скрипта каждый день в 01:05 кроме сб и вск). Для Linux - строчка для crontab; для Windows - команда schtasks.

#### Решение: Для того чтобы запускать этот скрипт каждый будний день в 01:05, необходимо добавить запись в crontab:

1. Открытие crontab -> crontab -e
2. Выбор текстового редактора
3. Создание записи -> 5 1 * * 0-5 /usr/bin/python3 /home/alexey/script.py, где 5 - минуты, 1 - часы, 0-5 дневной интервал, /usr/bin/python3 - Выбор интерпритатора, /home/alexey/script.py - выбор директории со скриптом
