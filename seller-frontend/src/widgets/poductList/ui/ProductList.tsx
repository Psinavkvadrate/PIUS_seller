import { Grid } from "@mui/material";
import { ProductCard } from "../../../entities/product/ui/ProductCard";
import { useGetMyProductsQuery } from "../../..//entities/product/api/productApi";

export const ProductList = ({ filters }) => {
  const normalizedFilters = {
    ...filters,
    search: filters.search || undefined,
    category: filters.category || undefined,
  };

  const { data } = useGetMyProductsQuery(normalizedFilters);

  return (
    <Grid container spacing={2}>
      {data?.items?.map((p) => (
        <Grid item xs={3} key={p.id}>
          <ProductCard product={p} />
        </Grid>
      ))}
    </Grid>
  );
};
