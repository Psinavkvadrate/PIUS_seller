import { Container } from "@mui/material";
import { useState } from "react";

import { OrdersFilters } from "../../widgets/filters/ui/OrdersFilters";
import { OrdersList } from "../../widgets/ordersList/ui/OrdersList";

export const SellerOrdersPage = () => {
  const [filters, setFilters] = useState({
    page: 1,
    limit: 10,
    status: "",
  });

  return (
    <Container maxWidth="xl">
      <OrdersFilters filters={filters} setFilters={setFilters} />

      <OrdersList filters={filters} />
    </Container>
  );
};