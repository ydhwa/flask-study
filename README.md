# Flask Study

## PythonApp
- [참고 사이트](https://code.tutsplus.com/ko/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972)
- Flask와 MySQL을 이용하여 간단한 회원가입 화면 구현
- 사이트와 다르게 구현한 점
   - 기존 사이트에서 적용한 jumbotron css의 링크가 변경되어 제대로 적용되지 않아 새로운 링크 추가(index.html, signup.html)
   - app.py에서 `from flask.ext.mysql import MySQL`로 호출하면 flask.ext 모듈을 찾을 수 없다는 에러 메시지가 뜸. 이를 `from flaskext.mysql import MySQL`로 수정함
   - `generate_password_hash`의 결과로 나온 password가 VARCHAR(45)의 데이터 길이를 넘는 문제가 발생하여, 테이블 생성 쿼리와 프로시저에 표기한 모든 데이터 양을 VARCHAR(100)으로 수정함


