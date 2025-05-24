## Dream E-commerce Platform

A fully functional and scalable e-commerce web application built using the MERN stack (MongoDB, Express.js, React.js, Node.js). Designed and developed independently to showcase end-to-end full-stack development skills, with clean architecture and modular code.

---

## 🚀 Tech Stack

- **Frontend:** HTML, CSS,JavaScript , React.js
- **Backend:** Node.js, Express.js  
- **Database:** MongoDB with Mongoose 
- **Tools & Utilities:** dotenv, vercel, netfly , Git & GitHub  

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

## 🧬 Clone the Repository

git clone https://github.com/Aksh4325/Dream-Ecommerce-Platform.git
cd Dream-Ecommerce-Platform

## 🚀 Setup Backend

cd backend
npm install

Create a .env file in the backend folder and add:

MONGO_URI=your_mongodb_connection_string
PORT=5000

Then run the backend server:

npm run dev


## 🚀 Setup Frontend

cd ../frontend
npm install
npm start

Frontend will start at: http://localhost:3000


---

## 🌐 Live Demo

Coming Soon – Deployment on Render / Vercel / Netlify + MongoDB Atlas

---

## 📷 Screenshots

Screenshots and demo GIFs will be added after frontend UI completion.

---

## 📌 Purpose

This project is designed to help beginners understand how real-world full-stack applications are developed, structured, and deployed. It includes basic functionality to get started and can be extended further with features like authentication, cart, payments, and admin dashboard.

---

## 👨‍💻 Author

Akshay Tiwari

GitHub: Aksh4325

LinkedIn: Akshay Tiwari

---

## Licence 

This project is licensed under the MIT License — feel free to use it for learning and development.

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

