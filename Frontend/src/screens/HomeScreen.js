import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function HomeScreen() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      const { data } = await axios.get("/api/products");
      setProducts(data);
    };
    fetchProducts();
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Product List</h2>
      {products.map((product) => (
        <div
          key={product._id}
          style={{
            border: "1px solid #ccc",
            margin: "1rem",
            padding: "1rem",
            borderRadius: "8px",
          }}
        >
          <Link to={`/product/${product._id}`} style={{ textDecoration: "none", color: "black" }}>
            <h3>{product.name}</h3>
          </Link>
          <p>Price: ₹{product.price}</p>
        </div>
      ))}
    </div>
  );
}

export default HomeScreen;
