import { Container, Typography, Box } from "@mui/material";

import { RevenueChart } from "../../widgets/revenue/ui/RevenueChart";
import { RevenueStats } from "../../widgets/revenue/ui/RevenueStats";
import { CompletedOrders } from "../../widgets/revenue/ui/CompletedOrders";

export const SellerRevenuePage = () => {
  return (
    <Container maxWidth="xl">
      <Typography variant="h4" mb={3}>
        Аналитика и выручка
      </Typography>

      <RevenueStats />

      <Box mt={4}>
        <RevenueChart />
      </Box>

      <Box mt={4}>
        <CompletedOrders />
      </Box>
    </Container>
  );
};