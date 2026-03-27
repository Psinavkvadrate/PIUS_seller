import { Box, TextField, MenuItem } from "@mui/material";

export const Filters = ({ filters, setFilters }) => {
  return (
    <Box display="flex" gap={2} mb={3}>
      <TextField
        label="Поиск"
        value={filters.search}
        onChange={(e) => setFilters({ ...filters, search: e.target.value })}
      />

      <TextField
        select
        label="Категория"
        value={filters.category || ""}
        onChange={(e) => setFilters({ ...filters, category: e.target.value })}
        sx={{ minWidth: 300 }}
      >
        <MenuItem value="">Все</MenuItem>
        <MenuItem value="electronics">Электроника</MenuItem>
        <MenuItem value="clothing">Одежда</MenuItem>
        <MenuItem value="food">Еда</MenuItem>
        <MenuItem value="home">Товары для дома</MenuItem>
        <MenuItem value="beauty">Уход</MenuItem>
        <MenuItem value="sports">Спорт</MenuItem>
        <MenuItem value="books">Книги</MenuItem>
        <MenuItem value="other">Другое</MenuItem>
      </TextField>
    </Box>
  );
};
