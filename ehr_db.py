import sqlite3
conn = sqlite3.connect('wo.db', check_same_thread=False)
conn1 = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c1 = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS detailstable(name TEXT, date TEXT,lift TEXT,weight TEXT, sets TEXT,time TEXT, sentiment TEXT, notes TEXT)')
def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS usertable(user_name TEXT, password TEXT)')

def add_data(name, date, lift, weight, sets,time, sentiment, notes):
	c.execute('INSERT INTO detailstable(name, date, lift, weight, sets,time, sentiment, notes) VALUES (?, ?,?,?,?,?,?, ?)',(name, date, lift, weight, sets,time, sentiment, notes))
	conn.commit()
    
def add_user(user_name, password):
	c.execute('INSERT INTO usertable(user_name, password) VALUES (?, ?)',(user_name, password))
	conn.commit()
    
def view_all_data():
	c.execute('SELECT * FROM detailstable')
	data = c.fetchall()
	return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def view_all_data_names():
	c.execute('SELECT DISTINCT name FROM detailstable')
	data = c.fetchall()
	return data

def get_name(name):
	c.execute('SELECT * FROM detailstable WHERE name="{}"'.format(name))
	data = c.fetchall()
	return data

def get_contact(contact):
	c.execute('SELECT * FROM detailstable WHERE contact="{}"'.format(contact))
	data = c.fetchall()

def edit_name_data(new_name, new_date, new_lift,new_weight, new_sets, new_time, new_sentiment, new_notes, name, date, lift, weight, sets,time, sentiment, notes):
	c.execute("UPDATE detailstable SET name = ?, date=?, lift = ?, weight = ?, sets = ?, time = ?, sentiment = ?, notes = ? WHERE date = ? and lift = ? and weight = ? and sets = ? and time = ? and sentiment = ? and notes = ? ",(new_name, new_date, new_lift,new_weight, new_sets, new_time, new_sentiment, new_notes, name, date, lift, weight, sets,time, sentiment, notes))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(name):
	c.execute('DELETE FROM detailstable WHERE name="{}"'.format(name))
	conn.commit()
    
