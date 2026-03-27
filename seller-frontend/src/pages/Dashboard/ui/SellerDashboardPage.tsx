import { Box, Button, Container } from "@mui/material";
import { useState } from "react";

import { Filters } from "../../../widgets/filters/ui/Filters";
import { ProductList } from "../../../widgets/poductList/ui/ProductList";
import { CreateProductModal } from "../../../features/product/ui/CreateProductModal";

export const SellerDashboardPage = () => {
  const [filters, setFilters] = useState({
    page: 1,
    limit: 12,
    search: "",
    category: "",
  });

  const [open, setOpen] = useState(false);

  return (
    <Container maxWidth="xl">
      <Filters filters={filters} setFilters={setFilters} />

      <ProductList filters={filters} />

      <Button
        variant="contained"
        onClick={() => setOpen(true)}
        sx={{
          position: "fixed",
          bottom: 40,
          right: 40,
        }}
      >
        + Добавить товар
      </Button>

      <CreateProductModal open={open} onClose={() => setOpen(false)} />
    </Container>
  );
};