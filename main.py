# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from database import get_db, engine
from models import Base, Product as ProductModel
from schemas import ProductCreate, Product, ProductUpdate
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # 데이터베이스 테이블 생성
        await conn.run_sync(Base.metadata.create_all)
    
    try:
        yield  # 여기에서 FastAPI 앱이 실행되는 동안 컨텍스트를 유지합니다.
    finally:
        # 비동기 데이터베이스 연결 종료
        await engine.dispose()
        
app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/products/", response_model=List[Product])
async def read_products(db: Session = Depends(get_db)): # 비동기 처리를 위해 async와 await 사용 둘은 항상 같이 다님
    result = await db.execute(select(ProductModel))
    products = result.scalars().all()
    return products
    
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[Product])
async def read_products(db: Session = Depends(get_db)):
    result = await db.execute(select(ProductModel))
    products = result.scalars().all()
    return products

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = result.scalars().first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    db_product = db_product.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for var, value in product.dict(exclude_unset=True).items():
        setattr(db_product, var, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = await db.execute(select(ProductModel).where(ProductModel.id == product_id))
    db_product = db_product.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"ok": True}

############# 4, 응답 및 상태 코드 연습 문제
# 1. 기본 GET 엔드포인트 생성
@app.get('/hello/')
def greeting():
    return {'message' : "Hello, LikeLion!"}

# 2. 간단한 사용자 정보 반환
@app.get("/user/{user_id}")
def get_user(user_id:int):
    return {"user_id":user_id, "name":"user name", "email":"user email"}

# 3. POST 요청 처리
@app.post("/students/")
def new_student(name:str, email:str):
    return {"name":name, "email":email}

from pydantic import BaseModel
class Student(BaseModel):
    name : str
    email : str

@app.post("/student/")
def new_stu(student:Student):
    return {"name":student.name, "email":student.email}


# 4. 항목삭제
@app.delete("items/{items_id}/")
def delete_item(item_id:int):
    return {"message":"item deleted"}

# 5. 조건부 응답
@app.get("/age/{age}")
def age_mg(age:int):
    if age > 18:
        return {"message":"adult"}
    else:
        return {"message":"child"}

# 6. 상태 코드 반환
@app.post("/create_student/", status_code=status.HTTP_201_CREATED)
def create_student(student:Student):
    return {"message":"성공", "student":student}

# 7. 리스트 반환
@app.get("/students/")
def load_stu():
    return {"student":[{"name":"lee", "email":"lee@com"}, {"name":"bang", "email":"bang@com"}]}

# 8. 응답 모델 사용
@app.get("/user/{user_id}", response_model=User)
def get_user(user_id:int):
    return {"name":"lee", "age":25}

# 9. 경로 파라미터와 쿼리 파라미터 조합
@app.get("/search/{keyword}")
def search_item(keyword:str):
    return 1

# 10. 커스텀 상태 코드와 에러 메세지
@app.get("/error")
def custom_error():
    raise HTTPException(status_code=400, detail="Invalid request")
