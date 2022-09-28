echo "=========== STARTING INSTALLATION =========== "
echo "ENV"
printenv
echo "==="
export VUE_APP_URL=wss://focused-meetings.azurewebsites.net/ws
cd /frontend
npm install
npm run build
mv dist /backend/app/dist
cd /backend/app
echo "ENV"
printenv
echo "==="
echo "=========== INSTALLATION DONE =========== "

uvicorn main:app --host 0.0.0.0 --port 80
