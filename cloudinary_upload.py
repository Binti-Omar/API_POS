import cloudinary
import cloudinary.uploader
from send_email import email

CLOUDINARY_URL="dftmzs33c"
API_KEY="172313466621985"
API_SECRET="aXrkWGdxt62F7sis3LMYrvPTap4"

cloudinary.config(
cloud_name = CLOUDINARY_URL,
api_key = API_KEY,
api_secret = API_SECRET
)

def upload_pdf(pdf_file):
    res = cloudinary.uploader.upload(f"receipts/{pdf_file}.pdf")

    print("this is cloudinary---------")
    print(res["secure_url"])
    email("chombobintiomar5@gmail.com","Payment Received",f"Thank You we have received your payment.Here is a link to your receipt-> {res['secure_url']}")
    return "success"

# upload_pdf("UE1692SFOZ")

