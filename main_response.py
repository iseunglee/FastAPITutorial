from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

# class User(BaseModel):
#     name: str
#     age: int

# @app.get("/user/{user_id}", response_model=User)
# def get_user(user_id: int):
#     # 실제 구현에서는 데이터베이스에서 사용자 정보를 조회하겠지만, 여기서는 예시 데이터를 사용합니다.
#     #return User(name="Alice", age=30)
#     return {"name":"Alice", "age":30, "more":"good"}

# 응답 및 상태코드 연습 문제
# 1번
@app.get("/hello/")
def greeting():
    return {"message" : "Hello, LikeLion!"}

# 2번
# 휴먼 클래스 만들어서 상속 사용해보기
class Human(BaseModel):
    #human_id : int
    name : str
    age : int
    email : str



users_list = []

# 여러명의 유저 만들기, 상태코드 설정 및 처리 활용
@app.post("/create_user/", status_code=status.HTTP_201_CREATED) # 유저 생성에는 id가 필요없음, 상태코드 설정
def make_user(user:Human): # 휴먼 클래스 상속받기
    hu1 = Human("name")
    user_list.append(hu1)
    return {"message" : "성공", "user" : user}


# 생성된 유저 확인해보기
@app.get("/user_list/")
def user_list(user:Human):
    pass

# Pydantic 자료형 검증 연습문제
# 1번
from datetime import datetime

class Event(BaseModel):
    name : str
    date : datetime
    attendees : int

@app.post("/evenets/")
def create_event(event : Event):
    return {"message" : "이벤트 틍록 성공", "event" : event}

# 2번
from datetime import date

class Book(BaseModel):
    title : str
    author : str
    borrowed_day : date

@app.post("/books/")
def record_book(book : Book):
    return {"message" : "도서 대출 성공", "book" : book}

# 3번
from pydantic import EmailStr

class ClubUser(BaseModel):
    name : str
    email : EmailStr
    register_day : date

@app.post("/clubuser/")
def register_member(clubuser : ClubUser):
    return {"message" : "회원 등록 성공", "clubuser" : clubuser}

# 4번
class Menu(BaseModel):
    name : str
    price : float
    give_day : date

@app.post("/menu/")
def register_menu(menu : Menu):
    return {"message" : "메뉴 등록 성공", "menu" : menu}

# 5번
class Group(BaseModel):
    name : str
    theme : str
    max_member : int

@app.post("/study-groups")
def create_study_group(study_group : Group):
    return {"message" : "성공", "group" : study_group}
