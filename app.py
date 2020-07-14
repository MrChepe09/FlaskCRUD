from flask import Flask, render_template, redirect, url_for, request, g
from database import get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def home():
    db = get_db()
    data_cur = db.execute('''select count(*) as user, count(distinct country) as countries,
                            sum(case when level='Alpha' then 1 else 0 end) as alpha,
                            sum(case when level='Beta' then 1 else 0 end) as beta,
                            sum(case when level='Gold' then 1 else 0 end) as gold
                            from users;''')
    data_res = data_cur.fetchone()
    print(data_cur, flush=True)

    return render_template('index.html', active='index', data=data_res)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if (request.method == 'POST'):
        db = get_db()
        user = db.execute('''select name from users where name = ? and country = ?''', [request.form['name'], request.form['country']])
        user_res = user.fetchone()
        if user_res:
            return render_template('add.html', active='add', error="fail")
        db.execute('''Insert into users 
                                (name, country, level)
                                values (?, ?, ?)''', [request.form['name'], request.form['country'], request.form['level']])
        db.commit()
        return render_template('add.html', active='add', error="success")
    return render_template('add.html', active='add', error=None)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if (request.method == 'POST'):
        db = get_db()
        user = db.execute('''select name from users where name = ? and country = ?''', [request.form['name'], request.form['country']])
        user_res = user.fetchone()
        if not user_res:
            return render_template('update.html', active='update', error="fail")
        db.execute('''update users set level = (?)
                      where name = (?) and country = (?)''', [request.form['level'], request.form['name'], request.form['country']])
        db.commit()
        return render_template('update.html', active='update', error="success")
    return render_template('update.html', active='update', error=None)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if (request.method == 'POST'):
        db = get_db()
        user = db.execute('''select name from users where name = ? and country = ?''', [request.form['name'], request.form['country']])
        user_res = user.fetchone()
        if not user_res:
            return render_template('delete.html', active='delete', error="fail")
        db.execute('''delete from users
                      where name = (?) and country = (?)''', [request.form['name'], request.form['country']])
        db.commit()
        return render_template('delete.html', active='delete', error="success")
    return render_template('delete.html', active='delete', error=None)

@app.route('/show', methods=['GET', 'POST'])
def show():
    return '<h1>Show</h1>'

if(__name__ == '__main__'):
    app.run(debug=True)