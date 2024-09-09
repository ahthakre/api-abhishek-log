import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI, HTTPException
import uvicorn

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(r'C:\Users\ES\OneDrive\Desktop\ADAS\log-object-detection-firebase-adminsdk-svcpu-2a933d9402.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://log-object-detection-default-rtdb.firebaseio.com/'
    })

# Create a FastAPI app
app = FastAPI()

# Route to get the latest object detection data from Firebase
@app.get("/api/get_latest_data")
async def get_latest_data():
    ref = db.reference('detections')
    data = ref.order_by_key().limit_to_last(1).get()  # Get the most recent entry
    if data:
        for key, value in data.items():
            return value
    raise HTTPException(status_code=404, detail="No data found")

# Route to get all the object detection data stored in Firebase
@app.get("/api/get_all_data")
async def get_all_data():
    ref = db.reference('detections')
    data = ref.get()
    if data:
        return data
    raise HTTPException(status_code=404, detail="No data found")

# Start the FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)  # Use "app:app" to reference the app instance
