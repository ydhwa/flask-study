from flask import Flask, render_template, json, request, redirect
from flaskext.mysql import MySQL
# 비밀번호에 salt 적용
from werkzeug import generate_password_hash, check_password_hash
# 사용자 홈페이지에 대한 허가되지 않은 접근 제한하기
from flask import session

mysql = MySQL()
app = Flask(__name__)

# Session key
app.secret_key = 'why would I tell you my secret key?'
# Default pagination setting
pageLimit = 2

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'database_user_id'
app.config['MYSQL_DATABASE_PASSWORD'] = 'database_user_password'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
	# /로 이동했음에도 로그인 세션이 켜져 있다면 userHome으로 이동시킴
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

# jQuery AJAX를 사용하여 등록 데이터 전송(회원가입)
@app.route('/signUp', methods=['POST','GET'])
def signUp():
	try:
		# read the posted values from the UI
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		# validate the received values
		if _name and _email and _password:
			# All Good, let's call MySQL
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(_password)
			cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit() 
				return json.dumps({'message':'User create successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})

	except Exception as e:
		return json.dumps({'error':str(e)})	
	finally:
		cursor.close()
		conn.close()


# 로그인 화면 보여줌
@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')

# 로그인 유효성 검증
@app.route('/validateLogin', methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']

		# connect to mysql
		con = mysql.connect()
		cursor = con.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		data = cursor.fetchall()

		if len(data) > 0:
			if check_password_hash(str(data[0][3]),_password):
				session['user'] = data[0][0]
				return redirect('/userHome')
			else:
				return render_template('error.html',error = 'Wrong Email address of Password.')
		else:
			return render_template('error.html',error = 'Wrong Email address of Password.')


	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		con.close()

# 허가되지 않은 접근 제한
@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html',error = 'Unauthorized Access')


# 로그아웃
@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')


# 버킷리스트에 추가하는 기능들
@app.route('/showAddWish')
def showAddWish():
	return render_template('addWish.html')
@app.route('/addWish',methods=['POST'])
def addWish():
	try:
		# 로그인이 되어 있는 상태인지 검증한 후 작업 진행
		if session.get('user'):
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']
			_user = session.get('user')

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addWish',(_title,_description,_user))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return redirect('/userHome')
			else:
				return render_template('error.html',error = 'An error occured!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		conn.close()

# 버킷리스트/버킷리스트 항목 조회
@app.route('/getWish', methods=['POST'])
def getWish():
	try:
		if session.get('user'):
			_user = session.get('user')
			_limit = pageLimit
			_offset = request.form['offset']
			_total_records = 0

			# Connect to MySQL and fetch data
			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_GetWishByUser',(_user,_limit,_offset,_total_records))
			wishes = cursor.fetchall()

			cursor.close()

			cursor = con.cursor()
			cursor.execute('SELECT @_sp_GetWishByUser_3')

			outParam = cursor.fetchall()

			# JSON으로 반환하기 쉽도록 버킷리스트를 딕셔너리에 저장
			response = []
			wishes_dict = []

			for wish in wishes:
				wish_dict = {
					'Id': wish[0],
					'Title': wish[1],
					'Description': wish[2],
					'Date': wish[4]}
				wishes_dict.append(wish_dict)

			response.append(wishes_dict)
			response.append({'total': outParam[0][0]})

			return json.dumps(response)
		else:
			return render_template('error.html', error='Unauthorized Access')
	except Exception as e:
		return render_template('error.html', error = str(e))
@app.route('/getWishById',methods=['POST'])
def getWishById():
	try:
		if session.get('user'):
			_id = request.form['id']
			_user = session.get('user')

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_GetWishById',(_id,_user))
			result = cursor.fetchall()

			wish = []
			wish.append({'Id': result[0][0], 'Title': result[0][1], 'Description': result[0][2]})

			return json.dumps(wish)
		else:
			return render_template('error.html', error = 'Unauthorized Access')	
	except Exception as e:
		return render_template('error.html', error = str(e))


# 버킷리스트 수정
@app.route('/updateWish', methods=['POST'])
def updateWish():
	try:
		if session.get('user'):
			_user = session.get('user')
			_title = request.form['title']
			_description = request.form['description']
			_wish_id = request.form['id']

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'status':'OK'})
			else:
				return json.dumps({'status':'ERROR'})
	except Exception as e:
		return json.dumps({'status':'Unauthorized access'})
	finally:
			cursor.close()
			conn.close()


# 버킷리스트 삭제
@app.route('/deleteWish', methods=['POST'])
def deleteWish():
	try:
		if session.get('user'):
			_id = request.form['id']
			_user = session.get('user')

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_deleteWish',(_id,_user))
			result = cursor.fetchall()

			if len(result) is 0:
				conn.commit()
				return json.dumps({'status':'OK'})
			else:
				return json.dumps({'status':'An Error occured'})
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return json.dumps({'status':str(e)})
	finally:
		cursor.close()
		conn.close()



if __name__ == "__main__":
    app.run(port=5002)


