import { Card, CardContent, Typography } from "@mui/material";
import { useState } from "react";
import { PRODUCT_CATEGORY_LABELS } from "../../../entities/product/model/productCategory";
import { ProductModal } from "../../../features/product/ui/ProductModal";

export const ProductCard = ({ product }) => {
  const [open, setOpen] = useState(false);

  const categoryLabel =
    PRODUCT_CATEGORY_LABELS[product.category] || product.category;

  return (
    <>
      <Card
        onClick={() => setOpen(true)}
        sx={{ cursor: "pointer" }}
      >
        <img src={product.img} style={{ height: 150, width: "100%" }} />

        <CardContent>
          <Typography>{product.name}</Typography>
          <Typography>{product.price} ₽</Typography>
          <Typography>Остаток: {product.available}</Typography>
          <Typography>{categoryLabel}</Typography>
        </CardContent>
      </Card>

      <ProductModal
        open={open}
        onClose={() => setOpen(false)}
        product={product}
      />
    </>
  );
};