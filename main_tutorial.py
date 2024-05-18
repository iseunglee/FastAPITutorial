from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "Sample Item"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item deleted"}

@app.get("/chatgpt/{text}")
def ai_system(text : str):
    # open ai chatgpt api를 이용해서 동작
    # 응답
    return {"message" : "응답"}

@app.get("/image/")
def ai_image(text : str):
    # 이미지 작업
    # 응답
    return {"message" : "응답"}

@app.get("/machinelearning/")
def ai_ml(text : str):
    # 어떤 작업
    # 응답
    return {"message" : "응답"}

@app.get("/robot/left/")
def ai_ml(text : str):
    # 로봇 왼쪽으로 움직이는 작업 코드
    # 응답
    return {"message" : "응답"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/likelion/{student_id}")
def check_student(student_id : int, name : str = None, email : str = None):
    if student_id == 1:
        name = '김멋사'
        email = 'kimmutsa@li.com'
    return {"student_id" : student_id, "name" : name, "email" : email}

@app.post("/projects/")
def register_pro_item(name : str, description : str):
    return {"name" : name , "description" : description}

@app.delete("/projects/{project_id}")
def delete_pro(project_id : int):
    return {"message" : f"{project_id}번 pro 매우 훌륭"}

# 강사님 답안
class Student(BaseModel):
    student_id : int
    name : str
    email : str

# 아이템 등록
@app.post("/item/")
def item_create(item:Item): # 위의 item 클래스 상속
    return {"name" : item.name, "description" : item.description}