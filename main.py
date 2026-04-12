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

@app.route('/',methods=allowed_methods)
def home():
    method = request.method.lower()

    if method == "get":
        return jsonify({"Flask API Version" : "1.0"}),200
    else:
        return jsonify({"message":"Method not allowed"}),405
    
@app.route("/register",methods=allowed_methods)
def register():
    try:
        method = request.method.lower()

        if method == "post":
            data = request.get_json()

            if data["full_name"] == "" or data["email"] == "" or data["password"] == "":
                return jsonify({"error" : "name,email and password cannot be empty"}),400
            
            existing_user = mysession.query(User).filter_by(email=data["email"]).first()

            if existing_user:
                return jsonify({"error":"Email already registered"}),409
            
            new_user = User(
                full_name=data['full_name'],
                email=data['email'],
                password=data['password'],
                created_at=datetime.utcnow()
            )

            mysession.add(new_user)
            mysession.commit()

            return jsonify({"message":"User registered successfully"}),201
        
        else:
            return jsonify({"msg":"Method not allowed"}),405
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/login',methods=allowed_methods)
def login():
    try:
        method = request.method.lower()

        if method == "post":
            data = request.get_json()

            email=data.get("email")
            password=data.get("password")

            if not email or not password:
                return jsonify({"error":"Email and password required"}),400

            query = select(User).where(User.email==email)  
            existing_user = mysession.scalars(query).first()

            if not existing_user:
                return{"error":"Invalid email"},401
            
            if not password:
                return{"error":"Invalid password"},401
            
            return jsonify({
                "message":"Login successful",
                "user": {
                    "id": existing_user.id,
                    "email":existing_user.email,
                    "password":existing_user.password
                }
            }),200
        
        else:
            return jsonify({"msg":"Method not allowed"}),405
    except Exception as e:
        return jsonify({"error":str(e)})
    
@app.route("/products",methods=allowed_methods)
def products():
    try:
        method = request.method.lower()

        if method == "get":
            query = select(Product) 
            products = mysession.scalars(query).all()

            product_list = []
            for i in products:
                product_list.append({
                "id" : i.id,
                "user_id": i.user_id,
                "name" : i.name,
                "amount" : i.amount,
                "created_at" : i.created_at 
                })

            return jsonify(product_list),200
        
        elif method == "post":
            data = request.get_json()

            user_id = data.get("user_id")
            name = data.get("name")
            amount = data.get("amount")

            if not user_id or not name or not amount:
                return({"error":"All fields are required"}),400
            
            new_product = Product(
            user_id = user_id,
            name = name,
            amount = float(amount)
            )

            mysession.add(new_product)
            mysession.commit()

            return jsonify({"message": "A new product has been created "}),201
        
        else:
            return jsonify({"error":"Method not allowed"}),405
        
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route("/sales",methods=allowed_methods)
def sales():
    try:
        method = request.method.lower()

        if method == "get":
            query = select(Sales) 
            sales = mysession.scalars(query).all()

            sales_list = []
            for i in sales:
                sales_list.append({
                "id" : i.id,
                "product_id": i.product_id,
                "created_at" : i.created_at 
                })

            return jsonify(sales_list),200
        
        elif method == "post":
            data = request.get_json()

            product_id = data.get("product_id")

            if not product_id:
                return({"error":"All fields are required"}),400
            
            new_sale = Sales(
            product_id = product_id,
            )

            mysession.add(new_sale)
            mysession.commit()

            return jsonify({"message": "A new sale has been madeed "}),201
        
        else:
            return jsonify({"error":"Method not allowed"}),405
        
    except Exception as e:
        return jsonify({"error":str(e)}),500

        










app.run(debug=True)