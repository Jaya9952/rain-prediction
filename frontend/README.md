 Start FastAPI Backend


 cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Open http://localhost:8000/docs to test the API.

Frontend Setup

cd frontend
npm install

start React Frontend

npm start


Final Checklist

1. Backend is running → uvicorn main:app --reload

2. API is accessible at → http://localhost:8000/docs

3. Frontend is running → npm start

4. React successfully sends inputs to API

5. Prediction is displayed correctly