import Product from "../models/Product.js";

// Sab products return karne wala function (already hai)
const getProducts = async (req, res) => {
  const products = await Product.find({});
  res.json(products);
};

// Single product return karne wala function (naya)
const getProductById = async (req, res) => {
  const product = await Product.findById(req.params.id);
  if (product) {
    res.json(product);
  } else {
    res.status(404).json({ message: "Product not found" });
  }
};

export { getProducts, getProductById };
