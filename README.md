# flask-study

## Python App
- [참고 사이트](https://code.tutsplus.com/ko/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972)
- 사이트와 다르게 구현한 점
   - jumbotron css 링크가 이전되어 새로운 링크를 불러옴(index.html, signup.html)
   - app.py에서 `from flask.ext.mysql import MySQL`을 하면 flask.ext 모듈을 찾을 수 없다는 메시지가 뜸. 이를 `from flaskext.mysql import MySQL`로 수정함
   - check_password_hash의 결과로 나오는 데이터의 양이 VARCHAR(45)에 담기에는 길어, MySQL의 모든 컬럼을 `VARCHAR(100)`으로 수정하였고, 프로시저도 수정함

