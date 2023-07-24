#!/usr/bin/python3

import os
import datetime
import subprocess
import sys

args = sys.argv

config = {}
with open(args[1],'r') as f:
    lines = f.readlines()
    for line in lines:
        key,value = line.strip().split('=')
        config[key] = value

DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']

BACKUP_PATH = config['BACKUP_PATH']
BACKUP_PREFIX = config['BACKUP_PREFIX']
BACKUP_COUNT = int(config['BACKUP_COUNT'])
                           
DATETIME_FORMAT = '%Y.%m.%d_%H%M%S'

# Формирование имени файла резервной копии
current_datetime = datetime.datetime.now().strftime(DATETIME_FORMAT)
backup_filename = f'{BACKUP_PREFIX}.{current_datetime}.tar.gz'
backup_filepath = os.path.join(BACKUP_PATH, backup_filename)

# Команда для выполнения резервного копирования
backup_command = f'pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -F t -f {backup_filepath}'

try:
    # Выполнение резервного копирования
    subprocess.check_output(backup_command, shell=True)
    
    # Удаление лишних файлов резервных копий
    backup_files = sorted(os.listdir(BACKUP_PATH))
    if len(backup_files) > BACKUP_COUNT:
        for file in backup_files[:len(backup_files) - BACKUP_COUNT]:
            os.remove(os.path.join(BACKUP_PATH, file))
    
    # Вывод сообщения об успешном выполнении
    print(f'Резервная копия базы данных {DB_NAME} успешно создана: {backup_filepath}')
    
except subprocess.CalledProcessError as e:
    # Обработка ошибок соединения и ошибок на стороне sql сервера
    error_type = 'Ошибка соединения' if e.returncode == 1 else 'Ошибка на стороне sql сервера'
    error_message = e.output.decode('utf-8').strip()
    error_datetime = datetime.datetime.now().strftime(DATETIME_FORMAT)
    
    # Вывод сообщения об ошибке
    print(f'{error_type}: {error_message} (возникло {error_datetime})')
    
    # Запись сообщения об ошибке в журнал
    log_filepath = os.path.join(BACKUP_PATH, f'{BACKUP_PREFIX}.{current_datetime}.log')
    with open(log_filepath, 'a') as log_file:
        log_file.write(f'{error_type}: {error_message} (возникло {error_datetime})\n')
