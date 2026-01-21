# =============================
# app.py (Complete ToDo App)
# =============================
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ---------- Database Config ----------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',   # change if needed
    'database': 'todo_db'
}

# ---------- DB Connection ----------
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ---------- Routes ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        task = request.form['task']
        cursor.execute("INSERT INTO todo (task) VALUES (%s)", (task,))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM todo ORDER BY id DESC")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todo WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        task = request.form['task']
        cursor.execute("UPDATE todo SET task=%s WHERE id=%s", (task, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM todo WHERE id=%s", (id,))
    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)

# =============================
# templates/index.html
# =============================
'''
<!DOCTYPE html>
<html>
<head>
    <title>ToDo App</title>
    <style>
        body { font-family: Arial; background:#f4f4f4; }
        .box { width:450px; margin:50px auto; background:white; padding:20px; }
        input { width:75%; padding:8px; }
        button { padding:8px; }
        li { margin:10px 0; }
        a { margin-left:10px; }
    </style>
</head>
<body>
<div class="box">
    <h2>ToDo List</h2>
    <form method="POST">
        <input type="text" name="task" placeholder="Enter task" required>
        <button>Add</button>
    </form>
    <ul>
        {% for t in tasks %}
            <li>
                {{ t[1] }}
                <a href="/update/{{ t[0] }}">Edit</a>
                <a href="/delete/{{ t[0] }}">Delete</a>
            </li>
        {% endfor %}
    </ul>
</div>
</body>
</html>
'''

# =============================
# templates/update.html
# =============================
'''
<!DOCTYPE html>
<html>
<head>
    <title>Update Task</title>
</head>
<body>
<h2>Update Task</h2>
<form method="POST">
    <input type="text" name="task" value="{{ task[1] }}" required>
    <button>Update</button>
</form>
</body>
</html>
'''
