import { type RouteObject } from "react-router-dom";
import { SellerDashboardPage } from "../../pages/Dashboard/ui/SellerDashboardPage";
import { SellerOrdersPage } from "../../pages/Orders/SellerOrdersPage";

export const routeConfig: RouteObject[] = [
  {
    path: "/",
    element: <SellerDashboardPage />,
  },
  {
    path: "/orders",
    element: <SellerOrdersPage />,
  },
];
