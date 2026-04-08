import { Card, CardContent, Typography } from "@mui/material";
import { useGetTotalRevenueQuery } from "../../../entities/order/api/orderApi";

export const RevenueStats = () => {
  const { data, isLoading } = useGetTotalRevenueQuery();

  if (isLoading) return <div>Загрузка...</div>;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Общая выручка</Typography>
        <Typography variant="h4">
          {data?.totalRevenue || 0} ₽
        </Typography>
      </CardContent>
    </Card>
  );
};