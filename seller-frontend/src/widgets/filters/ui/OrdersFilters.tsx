import { Box, TextField, MenuItem } from "@mui/material";
import { ORDER_STATUS_LABELS } from "../../../entities/order/model/orderStatus";

export const OrdersFilters = ({ filters, setFilters }) => {
  return (
    <Box mb={3}>
      <TextField
        select
        label="Статус"
        value={filters.status || ""}
        onChange={(e) =>
          setFilters({
            ...filters,
            status: e.target.value || undefined,
          })
        }
        sx={{ minWidth: 250 }}
      >
        <MenuItem value="">Все</MenuItem>

        {Object.entries(ORDER_STATUS_LABELS).map(([value, label]) => (
          <MenuItem key={value} value={value}>
            {label}
          </MenuItem>
        ))}
      </TextField>
    </Box>
  );
};