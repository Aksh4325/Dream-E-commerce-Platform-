import express from "express";
import { getProducts, getProductById } from "../controllers/productController.js";

const router = express.Router();

router.route("/").get(getProducts);             // Sab products ke liye
router.route("/:id").get(getProductById);      // Single product ke liye

export default router;
