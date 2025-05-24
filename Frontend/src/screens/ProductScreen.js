import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";

function ProductScreen() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      const { data } = await axios.get(`/api/products/${id}`);
      setProduct(data);
    };
    fetchProduct();
  }, [id]);

  if (!product) return <div>Loading...</div>;

  return (
    <div style={{ padding: "1rem" }}>
      <Link to="/">Back to Products</Link>
      <h2>{product.name}</h2>
      <p>Price: ₹{product.price}</p>
      <p>Description: {product.description}</p>
    </div>
  );
}

export default ProductScreen;
