import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  IconButton,
  MenuItem,
  TextField,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import TelegramIcon from "@mui/icons-material/Telegram";

import {
  useUpdateOrderStatusMutation,
  useDeleteOrderMutation,
} from "../api/orderApi";

import { ORDER_STATUS_LABELS } from "../model/orderStatus";
import { OrderModal } from "../../../features/order/ui/OrderModal";

export const OrderCard = ({ order }) => {
  const [updateStatus] = useUpdateOrderStatusMutation();
  const [deleteOrder] = useDeleteOrderMutation();
  const [openModal, setOpenModal] = useState(false);

  const handleStatusChange = async (newStatus) => {
    try {
      await updateStatus({
        id: order.id,
        status: newStatus,
      }).unwrap();
    } catch (e) {
      alert(e?.data?.detail || "Ошибка обновления статуса");
    }
  };

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (!confirm("Удалить заказ?")) return;

    try {
      await deleteOrder(order.id).unwrap();
    } catch (e) {
      alert("Ошибка удаления");
    }
  };

  const handleContact = (e) => {
    e.stopPropagation();
    if (!order.user?.telegram) return alert("Нет telegram");
    window.open(`https://t.me/${order.user.telegram}`, "_blank");
  };

  return (
    <>
      <Card
        onClick={() => setOpenModal(true)}
        sx={{ cursor: "pointer", mb: 2 }}
      >
        <CardContent>
          <Box display="flex" justifyContent="space-between">
            <Box>
              <Typography>№ {order.orderNumber}</Typography>
              <Typography>{order.totalAmount} ₽</Typography>
              <Typography>{order.deliveryAddress}</Typography>
            </Box>

            <Box display="flex" gap={1}>
              <IconButton onClick={handleContact}>
                <TelegramIcon />
              </IconButton>

              <IconButton onClick={handleDelete}>
                <DeleteIcon color="error" />
              </IconButton>
            </Box>
          </Box>

          <Box mt={2}>
            <TextField
              select
              label="Статус"
              value={order.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              size="small"
              fullWidth
            >
              {Object.entries(ORDER_STATUS_LABELS).map(([value, label]) => (
                <MenuItem key={value} value={value}>
                  {label}
                </MenuItem>
              ))}
            </TextField>
          </Box>
        </CardContent>
      </Card>

      <OrderModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        order={order}
      />
    </>
  );
};