import React, { useEffect, useState } from "react";
import axios from "axios";

const HomeScreen = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await axios.get(`${process.env.REACT_APP_API_URL}/products`);
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <main>
      <h2>Latest Products</h2>
      {products.length === 0 ? (
        <p>Loading products...</p>
      ) : (
        <ul>
          {products.map((product, index) => (
            <li key={index}>
              <h3>{product.name}</h3>
              <p>Price: ₹{product.price}</p>
              <p>{product.description}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
};

export default HomeScreen;
