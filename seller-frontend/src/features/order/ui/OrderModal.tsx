import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  List,
  ListItem,
  ListItemText,
  Box,
} from "@mui/material";

import { useGetOrderByIdQuery } from "../../../entities/order/api/orderApi";

export const OrderModal = ({ open, onClose, order }) => {
  const { data, isLoading } = useGetOrderByIdQuery(order?.id, {
    skip: !open || !order?.id,
  });

  if (!order) return null;

  const fullOrder = data || order;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Заказ № {fullOrder.orderNumber}</DialogTitle>

      <DialogContent dividers>
        {isLoading ? (
          <Typography>Загрузка...</Typography>
        ) : (
          <>
            <Box mb={2}>
              <Typography variant="subtitle1">
                Статус: {fullOrder.status}
              </Typography>
              <Typography variant="subtitle1">
                Сумма: {fullOrder.totalAmount} ₽
              </Typography>
              <Typography variant="subtitle1">
                Адрес доставки: {fullOrder.deliveryAddress}
              </Typography>
            </Box>

            <Typography variant="h6">Товары:</Typography>
            <List dense>
              {fullOrder.items?.map((item, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`ID товара: ${item.productId}`}
                    secondary={`Количество: ${item.quantity}, Цена: ${item.price} ₽`}
                  />
                </ListItem>
              ))}
            </List>
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} color="primary">
          Закрыть
        </Button>
      </DialogActions>
    </Dialog>
  );
};