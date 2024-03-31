from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

# Load tasks from file
def load_tasks():
    tasks.clear()
    try:
        with open('tasks.txt', 'r') as file:
            tasks.extend([line.strip() for line in file.readlines()])
    except FileNotFoundError:
        pass

# Save tasks to file
def save_tasks():
    with open('tasks.txt', 'w') as file:
        for task in tasks:
            file.write(task + '\n')

# Route to view tasks
@app.route('/')
def view_tasks():
    load_tasks()
    return render_template('tasks.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form['task']
    if new_task:
        tasks.append(new_task)
        save_tasks()
    return redirect(url_for('view_tasks'))

# Route to mark a task as done
@app.route('/done/<int:index>')
def mark_done(index):
    if 0 <= index < len(tasks):
        task = tasks[index]
        if not task.endswith(' (Done)'):
            tasks[index] += ' (Done)'
            save_tasks()
    return redirect(url_for('view_tasks'))

# Route to mark a task as undone
@app.route('/undone/<int:index>')
def mark_undone(index):
    if 0 <= index < len(tasks):
        task = tasks[index]
        if task.endswith(' (Done)'):
            tasks[index] = task[:-6]
            save_tasks()
    return redirect(url_for('view_tasks'))

# Route to delete a task
@app.route('/delete/<int:index>')
def delete_task(index):
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks()
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
