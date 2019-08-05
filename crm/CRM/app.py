from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

# Config # DEBUG:
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] ='localhost'
app.config['MYSQL_DATABASE_USER'] ='root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'equip_crm_db'
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template('index.html')

@app.route('/new_client', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        client_data = request.form

        client_name = client_data['client_name']
        city_name = client_data['city_name']
        # district_name = client_data['district_name']

        insert_one_in_one_table("client_tbl", "client_name", client_name)

        # city_id = get_id("cities_tbl", "city_name", city_name)
        # update_row("client_tbl", "city_id", city_id, "client_name", client_name)

        cityes_dict = update_dict("cities_tbl")
        try:
            city_id = cityes_dict[city_name]
            update_row("client_tbl", "city_id", city_id, "client_name", client_name)
        except KeyError:
            insert_one_in_one_table("cities_tbl", "city_name", city_name)
            cityes_dict = update_dict("cities_tbl")
            city_id = cityes_dict[city_name]
            update_row("client_tbl", "city_id", city_id, "client_name", client_name)

        return redirect('/')

    clients = select_all_from_one_table("client_tbl")
    cities = select_all_from_one_table("cities_tbl")
    districts = select_all_from_one_table("district_tbl")
    # if cities:
    #     return render_template('new_client.html', cities=cities)
    return render_template('new_client.html', clients=clients, cities=cities, districts=districts )

def get_id(table_name, value_name, value):
    dictionary = update_dict(table_name)
    id = -1;
    try:
        id = dictionary[value]
    except KeyError:
        insert_one_in_one_table(table_name, value_name, value)
        dictionary = update_dict(table_name)
        id = dictionary[value]
    return id

def update_dict(table_name):
    result = select_all_from_one_table(table_name)
    dictionary = dict(result)
    reverse_result = {value: key for key, value in dictionary.items()}
    return reverse_result

# Обновляем данные в одной строке
def update_row(table_name, column_name, value, filter_name, filter_value):
    request_string = "UPDATE `{}` SET `{}` = '{}' WHERE (`{}` = '{}')".format(table_name, column_name, value, filter_name, filter_value)
    insert_in_bd(request_string)
    return True


# Вводим одно новое значение в одну ячейку
def insert_one_in_one_table(table_name, column_name, value):
    request_string = "INSERT INTO `{}` (`{}`) VALUES('{}')".format(table_name, column_name, value)
    insert_in_bd(request_string)
    return True


# Получаем ID последней записи в базе - НЕ РАБОТАЕТ
# def get_last_id():
    last_insertion_id_int = -1
    conn = mysql.connect()
    cur = conn.cursor()
    resultValue = cur.execute("SELECT LAST_INSERT_ID()")
    if resultValue > 0:
        last_insertion_id_int = cur.fetchone()
        print(last_insertion_id_int)
    cur.close()
    return last_insertion_id_int


# Получаем все из одной таблицы и получаем кортеж кортежей или False
def select_all_from_one_table(table_name):
    insertion = "SELECT * FROM `{}`".format(table_name)
    return select_from_db(insertion)


# вводим новую запись/записи в таблицу/таблицы
def insert_in_bd(request_string):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(request_string)
    conn.commit()
    cur.close()
    return True


# Получаем инфо из таблицы/таблиц - получаем либо кортеж либо False
def select_from_db(request_string):
    conn = mysql.connect()
    cur = conn.cursor()
    resultValue = cur.execute(request_string)
    if resultValue > 0:
        data_in_tuples = cur.fetchall()
        cur.close()
        return data_in_tuples
    cur.close()
    return False


if __name__ == '__main__':
    app.run(debug=True)
