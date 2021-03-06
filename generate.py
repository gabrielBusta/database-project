import os
import sys
import psycopg2
import platform
import time
from colorama import init, Fore, Back


def main(first=False):
    start_time = time.time()
    os.system('python manage.py migrate --fake app zero')

    sys.stdout.write('Deleting contents of \'migrations\' directory... ')
    migrations_dir_content = os.listdir('./app/migrations')

    for name in migrations_dir_content:
        if name != '__init__.py':
            os.system('rm ./app/migrations/' + name)

    sys.stdout.write(Fore.GREEN + 'DONE\n')

    try:
        sys.stdout.write('Connecting to database server... ')
        connection = psycopg2.connect(user='postgres',
                                      host='127.0.0.1',
                                      port=5432,
                                      password='default')
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        sys.stdout.write(Fore.GREEN + 'DONE\n')

        sys.stdout.write('Fetching server cursor... ')
        cursor = connection.cursor()
        sys.stdout.write(Fore.GREEN + 'DONE\n')

        if not first:
            sys.stdout.write('Killing external connections to the play database... ')
            kill_external_connections = ('SELECT pg_terminate_backend(pid) '
                                         'FROM pg_stat_activity '
                                         'WHERE pid <> pg_backend_pid() AND datname = \'play\';')
            cursor.execute(kill_external_connections)
            sys.stdout.write(Fore.GREEN + 'OK\n')

            sys.stdout.write('Deleting the play database... ')
            cursor.execute('DROP DATABASE play;')
            sys.stdout.write(Fore.GREEN + 'OK\n')

        sys.stdout.write('Creating the play database... ')

        if platform.system() == 'Windows':
            initialize_play_db = ('CREATE DATABASE play '
                                  'WITH '
                                  'OWNER = postgres '
                                  'ENCODING = \'UTF8\' '
                                  'LC_COLLATE = \'English_United States.1252\' '
                                  'LC_CTYPE = \'English_United States.1252\' '
                                  'TABLESPACE = pg_default '
                                  'CONNECTION LIMIT = -1;')
        elif platform.system() == 'Darwin':
            initialize_play_db = ('CREATE DATABASE play '
                                  'WITH '
                                  'OWNER = postgres '
                                  'ENCODING = \'UTF8\' '
                                  'LC_COLLATE = \'en_US.UTF-8\' '
                                  'LC_CTYPE = \'en_US.UTF-8\' '
                                  'TABLESPACE = pg_default '
                                  'CONNECTION LIMIT = -1;')
        else:
            sys.stdout.write(Fore.RED + 'ERROR\n')
            sys.stdout.write(Fore.RED + 'Unsuported OS!\n')
            exit(1)

        cursor.execute(initialize_play_db)
        sys.stdout.write(Fore.GREEN + 'OK\n')

    except psycopg2.Error as e:
        sys.stdout.write(Fore.RED + 'ERROR\n')
        sys.stdout.write(Fore.RED + e.diag.message_primary + '\n')
        exit(1)

    os.system('python manage.py makemigrations app')

    os.system('python manage.py migrate')

    os.system('python countries.py')

    os.system('python artists.py')

    os.system('python albums.py')

    os.system('python recordings.py')

    os.system('python users.py')

    sys.stdout.write('Generating database schema... ')
    os.system('java -jar ./jar/schemaSpy_5.0.0.jar -t pgsql -db play -host 127.0.0.1 -u postgres -p default -o schema -dp ./jar/postgresql-9.4.1212.jre6.jar -s public -noads')

    seconds = time.time() - start_time
    minutes = seconds / 60.0
    sys.stdout.write('\n' + Fore.BLUE + 'Total execution time:\nseconds: ' + str(seconds) + '\nminutes: ' + str(minutes) + '\n')


if __name__ == '__main__':
    # initialize colorama
    init(autoreset=True)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'first':
            main(first=True)
    else:
        main()
