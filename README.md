




## Dream E-commerce Platform

A fully functional and scalable e-commerce web application built using the MERN stack (MongoDB, Express.js, React.js, Node.js). Designed and developed independently to showcase end-to-end full-stack development skills, with clean architecture and modular code.

---

## 🚀 Tech Stack

- **Frontend:** React, React Router, Axios  
- **Backend:** Node.js, Express.js  
- **Database:** MongoDB with Mongoose  
- **Tools & Utilities:** dotenv, nodemon, concurrently, Git & GitHub  

---

## ✅ Features

- Display products fetched from backend API  
- Product detail view with dynamic routing  
- Clean and responsive frontend using React  
- MongoDB integration with Mongoose  
- Organized file structure with modular codebase  
- Beginner-friendly and scalable design  

---

## 🧪 How to Run Locally

## 1. Clone the Repository

```bash
git clone https://github.com/Aksh4325/Dream-Ecommerce-Platform.git
cd Dream-Ecommerce-Platform


## 2. Setup Backend

cd backend
npm install

Create a .env file in the backend folder and add:

MONGO_URI=your_mongodb_connection_string
PORT=5000

Then run the backend server:

npm run dev


---

3. Setup Frontend

cd ../frontend
npm install
npm start

Frontend will start at: http://localhost:3000


---

## 📁 Project Structure

```bash
Dream-Ecommerce-Platform/
├── backend/
│   ├── server.js
│   ├── config/db.js
│   ├── models/Product.js
│   ├── routes/productRoutes.js
│   ├──controllers/productController.js
│   ├── data/products.js
│   ├── .env
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   └── screens/
│   │       ├── HomeScreen.js
│   │       └── ProductScreen.js
│   └── package.json

---



