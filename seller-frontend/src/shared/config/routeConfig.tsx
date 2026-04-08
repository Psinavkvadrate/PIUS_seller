import { type RouteObject } from "react-router-dom";
import { SellerDashboardPage } from "../../pages/Dashboard/ui/SellerDashboardPage";
import { SellerOrdersPage } from "../../pages/Orders/SellerOrdersPage";
import { SellerRevenuePage } from "../../pages/Revenue/SellerRevenuePage";

export const routeConfig: RouteObject[] = [
  {
    path: "/",
    element: <SellerDashboardPage />,
  },
  {
    path: "/orders",
    element: <SellerOrdersPage />,
  },
  {
    path: "/revenue",
    element: <SellerRevenuePage />
  }
];
