cd /frontend
npm install
npm run build
mv dist /backend/app/dist
cd /backend/app

uvicorn main:app --host 0.0.0.0 --port 80
