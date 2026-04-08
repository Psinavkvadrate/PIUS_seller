import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

import { useGetRevenueQuery } from "../../../entities/order/api/orderApi";

export const RevenueChart = () => {
  const { data, isLoading } = useGetRevenueQuery();

  if (isLoading) return <div>Загрузка графика...</div>;
  if (!data?.length) return <div>Нет данных</div>;

  const formatted = data.map((item) => ({
    date: new Date(item.date).toLocaleDateString(),
    revenue: item.revenue,
  }));

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <LineChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};