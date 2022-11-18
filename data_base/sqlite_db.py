import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('currencies.db')
    cur = base.cursor()
    if base:
        print('База данных подключена')
    base.execute('CREATE TABLE IF NOT EXISTS currencies(name TEXT PRIMARY KEY,'
                 ' url TEXT, class TEXT, callback TEXT PRIMARY KEY)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO currencies VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


def sql_read_to_buttons():
    global base, cur
    base = sq.connect('currencies.db')
    cur = base.cursor()
    tuple_list = list()
    for ret in cur.execute('SELECT * FROM currencies').fetchall():
        tuple_list.append((ret[0], ret[3]))
    return tuple_list


async def sql_delete_button(data):
    cur.execute('DELETE FROM currencies WHERE name == ?', (data,))
    base.commit()


def sql_callback_list():
    base = sq.connect('currencies.db')
    cur = base.cursor()
    list_without_tuples = list()
    buff = cur.execute('SELECT callback FROM currencies').fetchall()
    for i in buff:
        list_without_tuples.append(i[0])
    return list_without_tuples


def sql_name_list():
    base = sq.connect('currencies.db')
    cur = base.cursor()
    list_without_tuples = list()
    buff = cur.execute('SELECT name FROM currencies').fetchall()
    for i in buff:
        list_without_tuples.append(i[0])
    return list_without_tuples


def sql_get_string(data):
    base = sq.connect('currencies.db')
    cur = base.cursor()
    return cur.execute('SELECT url, class FROM currencies WHERE callback == ?', (data,)).fetchone()


def sql_get_name(data):
    base = sq.connect('currencies.db')
    cur = base.cursor()
    return cur.execute('SELECT name FROM currencies WHERE callback == ?', (data,)).fetchone()[0]
