from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import pickle
from fastapi.middleware.cors import CORSMiddleware
import logging
import aiocron
import aiohttp

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cron job to ping health endpoint every 10 minutes
@aiocron.crontab('*/10 * * * *')
async def self_ping():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://similaritemstp12.onrender.com/health') as response:
            logger.info(f"Health check response: {response.status}")

# Load data at startup
@app.on_event("startup")
async def startup_event():
    global df, tfidf_matrix, tfidf_vectorizer
    # df = pd.read_csv("Product_names_list.csv")
    tfidf_matrix = load_npz('product_names_tfidf.npz')

    # Load the previously fitted TfidfVectorizer if needed
    with open('tfidf_vectorizer.pkl', 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
    logger.info("Data and vectorizer loaded.")
'''
# Function to recommend similar products
def recommend_similar_products(product_name: str, df, tfidf_matrix):
    # Step 3: Vectorize the input product name
    input_vector = tfidf_vectorizer.transform([product_name])
    
    # Step 4: Calculate cosine similarity between the input vector and all item vectors
    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()
    
    # Step 5: Get the top 5 similar items (excluding the input item itself)
    similar_indices = cosine_similarities.argsort()[-6:-1][::-1]
    similar_items = df['Item'].iloc[similar_indices].tolist()
    
    return similar_items
'''

def recommend_similar_products(product_name: str, db: Session, tfidf_matrix):

    products = crud.get_products(db)
    df = pd.DataFrame([{"Item": p.product_name} for p in products])
    
    input_vector = tfidf_vectorizer.transform([product_name])

    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()

    similar_indices = cosine_similarities.argsort()[-6:-1][::-1]
    similar_items = df['Item'].iloc[similar_indices].tolist()
    
    return similar_items

# Endpoint to get product recommendations
@app.get("/recommendations/")
async def get_recommendations(product_name: str, db: Session = Depends(get_db)):
    similar_products = recommend_similar_products(product_name, db, tfidf_matrix)
    return {"similar_products": similar_products}
'''
async def get_recommendations(product_name: str):
    
    similar_products = recommend_similar_products(product_name, db, tfidf_matrix)
    return {"similar_products": similar_products}
'''
# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
