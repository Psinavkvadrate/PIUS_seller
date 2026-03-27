import {
  Dialog,
  DialogContent,
  TextField,
  Button,
  MenuItem,
  Box,
  Typography,
} from "@mui/material";
import { useState } from "react";

import { useCreateProductMutation } from "../../../entities/product/api/productApi";
import { PRODUCT_CATEGORY_LABELS } from "../../../entities/product/model/productCategory";

export const CreateProductModal = ({ open, onClose }) => {
  const [createProduct] = useCreateProductMutation();

  const [form, setForm] = useState({
    name: "",
    price: "",
    available: "",
    description: "",
    img: "",
    category: "",
  });

  const handleCreate = async () => {
    if (!form.name || !form.price || !form.available || !form.category) {
      alert("Заполни обязательные поля");
      return;
    }

    await createProduct({
      ...form,
      price: Number(form.price),
      available: Number(form.available),
    });

    onClose();

    // сброс формы
    setForm({
      name: "",
      price: "",
      available: "",
      description: "",
      img: "",
      category: "",
    });
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogContent>
        <Typography variant="h6" mb={2}>
          Добавить товар
        </Typography>

        <Box display="flex" flexDirection="column" gap={2}>
          <TextField
            label="Название"
            value={form.name}
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
          />

          <TextField
            label="Цена"
            type="number"
            value={form.price}
            onChange={(e) =>
              setForm({ ...form, price: e.target.value })
            }
          />

          <TextField
            label="Количество"
            type="number"
            value={form.available}
            onChange={(e) =>
              setForm({ ...form, available: e.target.value })
            }
          />

          <TextField
            label="Описание"
            multiline
            rows={3}
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
          />

          <TextField
            label="Картинка (URL)"
            value={form.img}
            onChange={(e) =>
              setForm({ ...form, img: e.target.value })
            }
          />

          <TextField
            select
            label="Категория"
            value={form.category}
            onChange={(e) =>
              setForm({ ...form, category: e.target.value })
            }
          >
            {Object.entries(PRODUCT_CATEGORY_LABELS).map(
              ([value, label]) => (
                <MenuItem key={value} value={value}>
                  {label}
                </MenuItem>
              )
            )}
          </TextField>

          {form.img && (
            <img
              src={form.img}
              style={{ width: "100%", borderRadius: 8 }}
            />
          )}

          <Button variant="contained" onClick={handleCreate}>
            Создать
          </Button>
        </Box>
      </DialogContent>
    </Dialog>
  );
};