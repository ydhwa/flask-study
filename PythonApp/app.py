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

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = '####'
app.config['MYSQL_DATABASE_PASSWORD'] = '####'
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
				print(data[0][0], data[0][3])
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
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		conn.close()


@app.route('/getWish')
def getWish():
	try:
		if session.get('user'):
			_user = session.get('user')

			# Connect to MySQL and fetch data
			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_GetWishByUser',(_user,))
			wishes = cursor.fetchall()

			# JSON으로 반환하기 쉽도록 버킷리스트를 딕셔너리에 저장
			wishes_dict = []
			for wish in wishes:
				wish_dict = {
					'Id': wish[0],
					'Title': wish[1],
					'Description': wish[2],
					'Date': wish[4]}
				wishes_dict.append(wish_dict)

			return json.dumps(wishes_dict)
		else:
			return render_template('error.html', error='Unauthorized Access')
	except Exception as e:
		return render_template('error.html', error = str(e))


if __name__ == "__main__":
    app.run(port=5002)


