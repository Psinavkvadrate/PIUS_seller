import { type ReactNode } from "react";
import { Box } from "@mui/material";
import styles from "./MainLayout.module.css";
import { Header } from "../../widgets/header/ui/Header";
import { Footer } from "../../widgets/footer/ui/Footer";
import { useGetMyMarketQuery } from "../../entities/market/api/marketApi";

interface Props {
  children: ReactNode;
}

export const MainLayout = ({ children }: Props) => {
  const { data } = useGetMyMarketQuery(undefined);
  const userName = data?.marketName;

  return (
    <Box className={styles.background}>
      <Box className={styles.container}>
        <Header userName={userName} />

        <Box sx={{ flex: 1 }}>{children}</Box>

        <Footer />
      </Box>
    </Box>
  );
};
