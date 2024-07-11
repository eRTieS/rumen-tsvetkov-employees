import os

from flask import Flask, flash, redirect, render_template, request, url_for

from employee.common import allowed_file
from employee.const import UPLOAD_FOLDER
from employee.employees import EmployeesExecutor


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


employees_executor = EmployeesExecutor()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('read_file', filename=file.filename))
    return redirect(url_for('index'))


@app.route('/file/<filename>')
def read_file(filename):
    employees_executor.read_employees_data(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('index.html', employees=employees_executor.employees_controller.employees)


@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)


@app.route('/longest_period_pair')
def longest_period_pair():
    if employees_executor.employees_controller is None:
        return render_template(
            'longest_period_pair.html',
            pair={'employee_1': None, 'employee_2': None, 'days': None}
        )
    pair = employees_executor.employees_controller.find_longest_pair()

    return render_template('longest_period_pair.html', pair=pair)


@app.route('/employee/<employee_id>')
def employee(employee_id):
    if employees_executor.employees_controller is None:
        employees = [{
            'emp_id': None,
            'project_id': None,
            'date_from': None,
            'date_to': None,
            'days': None
        }]
    else:
        employees = employees_executor.employees_controller.get_projects_by_employee(employee_id)
    return render_template('employee.html', employees=employees)


@app.route('/project/<project_id>')
def project(project_id):
    if employees_executor.employees_controller is None:
        projects = [{
            'emp_id': None,
            'project_id': None,
            'date_from': None,
            'date_to': None,
            'days': None
        }]
        pair = {'employee_1': None, 'employee_2': None, 'days': None}
    else:
        projects = employees_executor.employees_controller.get_employees_by_project_id(project_id)
        pair = employees_executor.employees_controller.longest_employee_pair(projects)
    return render_template('project.html', employees=projects, pair=pair)
