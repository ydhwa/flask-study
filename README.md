# Flask Study

## 1. Flask와 MySQL을 이용하여 간단한 회원가입 화면 구현
- [참고 사이트](https://code.tutsplus.com/ko/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972)
- QUERY: Make table(user_tbl) and procedure(sign up).sql
- 비고
   - 기존 사이트에서 적용한 jumbotron css의 링크가 변경되어 제대로 적용되지 않아 새로운 링크 추가(index.html, signup.html)
   - app.py에서 `from flask.ext.mysql import MySQL`로 호출하면 flask.ext 모듈을 찾을 수 없다는 에러 메시지가 뜸. 이를 `from flaskext.mysql import MySQL`로 수정함
   - `generate_password_hash`의 결과로 나온 password가 VARCHAR(45)의 데이터 길이를 넘는 문제가 발생하여, 테이블 생성 쿼리와 프로시저에 표기한 모든 데이터 양을 VARCHAR(100)으로 수정함

## 2. 로그인 및 로그아웃 기능 구현, 페이지에 대한 허가되지 않은 접근 제한
- [참고 사이트](https://code.tutsplus.com/ko/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-2--cms-22999)
- QUERY: Make procedure(check validation).sql
- 비고
   - 회원가입 이후 리다이렉트를 제대로 구현하지 않음(일단 회원가입 상태를 표현할 수 있는 공간을 생성하고(`<div class="signupStatus">{{signupStatus}}</div>`), CSS도 적용해 둠). 즉, Sign up 이후 성공 여부는 console로만 확인할 수 있음
   - 바로 '/'로 이동 시 user 세션이 아직 유지되고 있다면 userHome으로 리다이렉트 시킴

## 3. 버킷리스트 추가 및 조회 기능 구현
- [참고 사이트](https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-3--cms-23120)
- QUERY: Make table(tbl_wish) and procedure(add and show bucket list).sql

## 4. 버킷리스트 수정 및 삭제 기능 구현
- [참고 사이트](https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-4--cms-23187)
- QUERY: Make procedure(inquery, edit and delete wish item).sql

## 5. 페이지네이션 구현
- [참고 사이트](https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-5--cms-23384)
- QUERY: Make procedure(inquery with pagination).sql
- 비고
   - 참고 사이트의 쿼리에서 `DEALLOCATE PREPARE stmt1`이라는 부분이 있는데, `stmt1`은 오타임. 따라서 이를 `stmt`로 수정하였음