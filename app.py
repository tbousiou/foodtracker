from flask import Flask, render_template, g, request
from datetime import datetime
from database import connect_db, get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


#App Routes
@app.route('/', methods = ['GET', 'POST'])
def index():
	db = get_db()

	if request.method == 'POST':
		user_date = request.form['entry-date'] 

		db.execute('insert into log_date (entry_date) values (?)', [user_date])
		db.commit()

	#query = 'select entry_date from log_date order by entry_date desc'
	query = """	select log_date.entry_date,
				sum(food.protein) as sumprotein,
    			sum(food.carbohydrates) as sumcarbohydrates,
			    sum(food.fat) as sumfat,
			    sum(food.calories) as sumcalories
				from food
				join food_date
				on food.id = food_date.food_id
				join log_date
				on log_date.id = food_date.log_date_id
				group by log_date.entry_date
				order by log_date.entry_date desc
	 		"""
	cur = db.execute(query)
	results = cur.fetchall()
	# This is very long FIX IT!
	log_dates = [ {'pretty_date': datetime.strftime(datetime.strptime(day['entry_date'], '%Y-%m-%d'), '%B %d, %Y'), 'entry_date': day['entry_date'], 'sumprotein': day['sumprotein'], 'sumcarbohydrates': day['sumcarbohydrates'], 'sumfat': day['sumfat'], 'sumcalories': day['sumcalories'] } for day in results ]
	return render_template('home.html', log_dates=log_dates)

@app.route('/view/<date>', methods = ['GET', 'POST'])
def view(date):
	db = get_db()

	cur = db.execute('select id, entry_date from log_date where entry_date = ?', [date])

	date_result = cur.fetchone()
	current_day_id = date_result['id']
	entry_date = date_result['entry_date']

	if request.method == 'POST':
		db.execute('insert into food_date (food_id, log_date_id) values (?, ?)', [request.form['food-select'], current_day_id])
		db.commit()

	pretty_date = datetime.strftime(datetime.strptime(date_result['entry_date'], '%Y-%m-%d'), '%B %d, %Y')
	
	food_cur = db.execute('select id, name from food')
	food_results = food_cur.fetchall()

	log_query = """select food.name, food.protein, food.carbohydrates, food.fat, food.calories
					 from food
					 join food_date
					 on food.id = food_date.food_id
					 WHERE food_date.log_date_id = ?"""

	log_cur = db.execute(log_query, [current_day_id] )
	log_results = log_cur.fetchall()

	total_protein = sum([x['protein'] for x in log_results])
	total_carbohydrates = sum([x['carbohydrates'] for x in log_results])
	total_fat = sum([x['fat'] for x in log_results])
	total_calories = sum([x['calories'] for x in log_results])
	
	return render_template('day.html', pretty_date=pretty_date, entry_date=entry_date, \
	 food_results=food_results, log_results=log_results, \
	 total_protein=total_protein, total_carbohydrates=total_carbohydrates, total_fat=total_fat, total_calories=total_calories)

@app.route('/food', methods = ['GET', 'POST'])
def food():
	db = get_db()

	if request.method == 'POST':
		name = request.form['food-name']
		protein = int(request.form['protein'])
		carbohydrates = int(request.form['carbohydrates'])
		fat = int(request.form['fat'])

		calories = protein * 4 + carbohydrates * 4 + fat * 9

		query = 'insert into food (name, protein, carbohydrates, fat, calories) values (?, ?, ?, ?, ?)'
		db.execute(query, [name, protein, carbohydrates, fat, calories])
		db.commit()

	query = 'select name, protein, carbohydrates, fat, calories from food'
	cur = db.execute(query)
	foods = cur.fetchall()

	return render_template('add_food.html', foods=foods)

if __name__ == '__main__':
	app.run(debug=True)
