import React from "react";
import { useParams } from "react-router-dom";
import products from "../products";

function ProductScreen() {
  const { id } = useParams();
  const product = products[id];

  return (
    <div style={{ padding: "1rem" }}>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <h4>Price: ₹{product.price}</h4>
    </div>
  );
}

export default ProductScreen;
