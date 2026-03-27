import {
  Dialog,
  DialogContent,
  Typography,
  TextField,
  IconButton,
  Box,
} from "@mui/material";
import { useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import SaveIcon from "@mui/icons-material/Save";

import {
  useUpdateProductMutation,
  useDeleteProductMutation,
} from "../../../entities/product/api/productApi";

export const ProductModal = ({ open, onClose, product }) => {
  const [isEdit, setIsEdit] = useState(false);

  const [form, setForm] = useState({
    name: product.name,
    price: product.price,
    available: product.available,
    description: product.description || "",
    img: product.img || "",
  });

  const [updateProduct] = useUpdateProductMutation();
  const [deleteProduct] = useDeleteProductMutation();

  const handleSave = async () => {
    await updateProduct({
      id: product.id,
      ...form,
    });

    setIsEdit(false);
  };

  const handleDelete = async () => {
    if (!confirm("Удалить товар?")) return;

    await deleteProduct(product.id);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogContent>
        <Box display="flex" justifyContent="flex-end" gap={1}>
          <IconButton onClick={() => setIsEdit(!isEdit)}>
            <EditIcon />
          </IconButton>

          <IconButton onClick={handleDelete}>
            <DeleteIcon color="error" />
          </IconButton>

          {isEdit && (
            <IconButton onClick={handleSave}>
              <SaveIcon />
            </IconButton>
          )}
        </Box>

        <Box display="flex" flexDirection="column" gap={2}>
          <TextField
            label="Название"
            value={form.name}
            disabled={!isEdit}
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
          />

          <TextField
            label="Цена"
            type="number"
            value={form.price}
            disabled={!isEdit}
            onChange={(e) =>
              setForm({ ...form, price: Number(e.target.value) })
            }
          />

          <TextField
            label="Количество"
            type="number"
            value={form.available}
            disabled={!isEdit}
            onChange={(e) =>
              setForm({ ...form, available: Number(e.target.value) })
            }
          />

          <TextField
            label="Описание"
            value={form.description}
            disabled={!isEdit}
            multiline
            rows={3}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
          />

          <TextField
            label="Картинка (URL)"
            value={form.img}
            disabled={!isEdit}
            onChange={(e) =>
              setForm({ ...form, img: e.target.value })
            }
          />

          {form.img && (
            <img
              src={form.img}
              style={{ width: "100%", borderRadius: 8 }}
            />
          )}

          <Typography>
            Категория: {product.category}
          </Typography>
        </Box>
      </DialogContent>
    </Dialog>
  );
};