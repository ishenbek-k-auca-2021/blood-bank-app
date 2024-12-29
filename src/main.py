from flask import Flask, render_template, request, redirect, flash
from database import init_db, add_donor, get_donors, delete_donor, get_donor_by_id, update_donor, get_filtered_donors


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the database when the app starts
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_type = request.form['blood_type']
        contact = request.form['contact']

        # Field validation
        if not name or not age or not blood_type or not contact:
            flash('Please fill in all fields', 'error')
            return render_template('register.html')

        try:
            age = int(age)
        except ValueError:
            flash('Age must be a number', 'error')
            return render_template('register.html')

        # Save donor to the database
        add_donor(name, age, blood_type, contact)
        flash('Registration successful!', 'success')
        return redirect('/donors')

    return render_template('register.html')


@app.route('/donors', methods=['GET'])
def donors():
    name = request.args.get('name')
    age = request.args.get('age')
    blood_type = request.args.get('blood_type')

    # Если возраст передан, то преобразуем его в число
    if age:
        try:
            age = int(age)
        except ValueError:
            flash('Age must be a number', 'error')
            age = None

    # Получаем всех доноров с учётом фильтров
    all_donors = get_filtered_donors(name, age, blood_type)
    return render_template('donors.html', donors=all_donors)

@app.route('/delete_donor/<int:donor_id>', methods=['POST'])
def delete_donor_route(donor_id):
    delete_donor(donor_id)
    return redirect('/donors')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/edit_donor/<int:donor_id>', methods=['GET', 'POST'])
def edit_donor(donor_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_type = request.form['blood_type']
        contact = request.form['contact']

        # Обновить информацию о доноре в базе данных
        update_donor(donor_id, name, age, blood_type, contact)
        flash('Donor information updated successfully!', 'success')
        return redirect('/donors')

    donor = get_donor_by_id(donor_id)
    return render_template('edit_donor.html', donor=donor)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
