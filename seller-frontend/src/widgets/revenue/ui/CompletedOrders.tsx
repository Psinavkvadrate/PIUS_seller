import {
  Card,
  CardContent,
  Typography,
  Box,
} from "@mui/material";

import { useGetCompletedOrdersQuery } from "../../../entities/order/api/orderApi";

export const CompletedOrders = () => {
  const { data, isLoading } = useGetCompletedOrdersQuery();

  if (isLoading) return <div>Загрузка...</div>;
  if (!data?.length) return <div>Нет завершённых заказов</div>;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" mb={2}>
          Завершённые заказы
        </Typography>

        <Box display="flex" flexDirection="column" gap={1}>
          {data.map((order) => (
            <Box
              key={order.id}
              display="flex"
              justifyContent="space-between"
            >
              <span>№ {order.orderNumber}</span>
              <span>{order.totalAmount} ₽</span>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};