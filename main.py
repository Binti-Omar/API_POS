from flask import Flask,request,jsonify
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker
from database import Base,User,Product,Payment,Sales
from flask_cors import CORS
from datetime import datetime
from mpesa import make_stk_push

app = Flask(__name__)
app.config["JWT_SECRET_KEY"]="nbgkkjhw654"

CORS(app)

jwt=JWTManager(app)

bcrypt=Bcrypt(app)

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
            
            hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            new_user = User(
                full_name=data['full_name'],
                email=data['email'],
                hashed_pw=hashed_pw,
                created_at=datetime.utcnow()
            )

            mysession.add(new_user)
            mysession.commit()

            token=create_access_token(identity=data['email'])

            return jsonify({"message":"User registered successfully","token":f"{token}"}),201
        
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
            
            if not bcrypt.check_password_hash(existing_user.hashed_pw,password):
                return{"error":"Invalid password"},401
            
            token=create_access_token(identity=data['email'])
            
            return jsonify({
                "message":"Login successful",
                "user": {
                    "id": existing_user.id,
                    "email":existing_user.email,
                    "full_name":existing_user.full_name
                     },
                    "token":f"{token}"
            }),200
        
        else:
            return jsonify({"msg":"Method not allowed"}),405
    except Exception as e:
        return jsonify({"error":str(e)})
    
@app.route("/products",methods=allowed_methods)
@jwt_required()
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
@jwt_required()
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
            product_id = product_id
            )

            mysession.add(new_sale)
            mysession.commit()

            return jsonify({"message": "A new sale has been made "}),201
        
        else:
            return jsonify({"error":"Method not allowed"}),405
        
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/stk-push',methods = allowed_methods)
def stk_push():
    try:
        data = request.get_json()

        # create a payment with only id,saleid,mrid,crid,created at
        sale_id = data.get('sale_id')
        trans_amount = data.get('amount')
        phone_paid = data.get('phone_number')

        if sale_id == None or trans_amount == None or  phone_paid == None:
            return jsonify({"error": "sale_id, phone_number and amount are required"}), 400
        
        stk_response = make_stk_push({
            "phone_number": phone_paid,
            "amount": trans_amount
        })
        print(stk_response)
        
        new_payment = Payment(
            sale_id=sale_id,
            mrid=stk_response.get("MerchantRequestID"),
            crid=stk_response.get("CheckoutRequestID"),
            phone_paid=phone_paid,
            trans_amount=float(trans_amount),
            status="Pending"
        )

        mysession.add(new_payment)
        mysession.commit()

        return jsonify({
            "message": "STK push sent",
            "response": stk_response,
            "phone_number": phone_paid,
            "amount": trans_amount
        }), 200
        
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/stk-call-back',methods = allowed_methods)
def call_back():
    data = request.get_json()
    print("stk callback data:-----------------",data)

    # fetch the payment record using mrid and crid
    query = select(Payment).where(Payment.mrid==data['Body']['stkCallback']['MerchantRequestID'],Payment.crid==data['Body']['stkCallback']['CheckoutRequestID'])  
    existing_payment = mysession.scalars(query).first()

    # update payment record with transaction code,transaction amount and status
    existing_payment.trans_code = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    mysession.commit()
    
    return jsonify({"message":"callback received"}),200

@app.route('/mpesa-payments', methods=allowed_methods)
def mpesa_payments():
    try:
        method = request.method.lower()
        if method == 'get':
            query = select(Payment)
            payments = mysession.scalars(query).all()

            result = []

            for p in payments:
                result.append({
                    "id": p.id,
                    "sale_id": p.sale_id,
                    "mrid": p.mrid,
                    "crid": p.crid,
                    "trans_code": p.trans_code,
                    "trans_amount": p.trans_amount,
                    "phone_paid": p.phone_paid,
                    "status": p.status,
                    "created_at": p.created_at
                })

            return jsonify(result), 200
        else:
            return jsonify({"error":"Method not allowed"}),405

    except Exception as e:
        return jsonify({"error": str(e)}), 500



app.run(debug=True)