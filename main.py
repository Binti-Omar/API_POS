from flask import Flask,request,jsonify
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker
from database import Base,User,Product,Payment,Sales
from datetime import datetime

app = Flask(__name__)

DATABASE_URL= "postgresql+psycopg2://postgres:C0717824020@localhost:5432/api_pos"

engine = create_engine(DATABASE_URL,echo=False)

session = sessionmaker(bind=engine)
mysession = session()

Base.metadata.create_all(engine)

allowed_methods = ['GET','POST','DELETE','PATCH']


app.run(debug=True)