from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from google.cloud.sql.connector import Connector
import sqlalchemy
import os

def embed_text(
    texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
    task: str = "RETRIEVAL_DOCUMENT",
    model_name: str = "text-embedding-004",
    dimensionality: Optional[int] = 256,
) -> List[List[float]]:
    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)
    return [embedding.values for embedding in embeddings]

# return top 3 recommeded product category
def get_suggeted_catagories(data):
    # data = ["Men's fashion > Activewear > Footwear > Sneakers"]
    output = embed_text(texts=data)
    pool = get_conn_pool()
    query = sqlalchemy.text("SELECT category, cosine_distance(embedding,string_to_vector(:e)) dist FROM product_category ORDER BY dist LIMIT 3;")
    categories = []
    try:
        with pool.connect() as db_conn:
            result = db_conn.execute(query,{"e":str(output[0])})
       # show results
        for row in result:
            print(row[0]) 
            print(row[1]) 
            categories.append(row[0])
        return categories            
    except Exception as e:
        print(e)    
    # finally:
        # cleanup()

# init
def init_connector():
    connector = Connector()
    return connector

connector = init_connector()

def get_connection():
    print('get connection')

    conn = connector.connect(
        os.environ['INSTANCE_CONNECTION_NAME'],
        "pymysql",
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        port="3306",
        db=os.environ['DB_NAME']
    )
    return conn

def get_conn_pool():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=get_connection,
    )
    return pool  



def cleanup():
    print("close connector")
    connector.close()


