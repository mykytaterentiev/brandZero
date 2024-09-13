from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import conn
from embeddings import generate_embedding

app = FastAPI()

class Transaction(BaseModel):
    merchant_name: str
    city: str
    mcc: str
    country: str

@app.get("/")
def read_root():
    if conn:
        return {"message": "Connected to PostgreSQL!"}
    else:
        return {"message": "Failed to connect to PostgreSQL"}

@app.post("/add-transaction")
def add_transaction(transaction: Transaction):
    if conn:
        try:
            embedding = generate_embedding(transaction.merchant_name)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO transactions (merchant_name, city, mcc, country, embedding) VALUES (%s, %s, %s, %s, %s)",
                (transaction.merchant_name, transaction.city, transaction.mcc, transaction.country, embedding)
            )
            conn.commit()
            return {"message": "Transaction added successfully with embedding!"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error adding transaction: {e}")
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

@app.get("/transactions")
def get_transactions():
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions")
        transactions = cur.fetchall()
        return {"transactions": transactions}
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

@app.post("/generate-transaction-embeddings")
def generate_transaction_embeddings():
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, merchant_name FROM transactions WHERE embedding IS NULL")
            transactions = cur.fetchall()
            
            for transaction in transactions:
                transaction_id = transaction[0]
                merchant_name = transaction[1]
                
                embedding = generate_embedding(merchant_name)

                cur.execute(
                    "UPDATE transactions SET embedding = %s WHERE id = %s",
                    (embedding, transaction_id)
                )
            
            conn.commit()
            return {"message": "Embeddings generated for all transactions!"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error generating embeddings: {e}")
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

@app.post("/generate-brand-embeddings")
def generate_brand_embeddings():
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM brands WHERE embedding IS NULL") 
            brands = cur.fetchall()
            
            for brand in brands:
                brand_id = brand[0]
                brand_name = brand[1] 

                embedding = generate_embedding(brand_name)
                
                cur.execute(
                    "UPDATE brands SET embedding = %s WHERE id = %s",
                    (embedding, brand_id)
                )
            
            conn.commit()
            return {"message": "Embeddings generated for all brands!"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error generating brand embeddings: {e}")
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
