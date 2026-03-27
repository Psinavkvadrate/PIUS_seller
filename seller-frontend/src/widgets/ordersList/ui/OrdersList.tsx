import { Box } from "@mui/material";
import { useGetOrdersQuery } from "../../../entities/order/api/orderApi";
import { OrderCard } from "../../../entities/order/ui/OrderCard";

export const OrdersList = ({ filters }) => {
  const cleanFilters = {
    ...filters,
    status: filters.status || undefined,
  };

  const { data } = useGetOrdersQuery(cleanFilters);

  return (
    <Box display="flex" flexDirection="column" gap={2}>
      {data?.orders?.map((order) => (
        <OrderCard key={order.id} order={order} />
      ))}
    </Box>
  );
};