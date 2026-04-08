import { baseApi } from "../../../shared/api/baseApi";

export const orderApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // GET /api/seller/orders
    getOrders: builder.query({
      query: ({ page = 1, limit = 10, status }) => ({
        url: "/seller/orders",
        params: { page, limit, status },
      }),
      providesTags: ["Orders"],
    }),

    // GET /api/seller/orders/{id}
    getOrderById: builder.query({
      query: (id) => `/seller/orders/${id}`,
      providesTags: ["Orders"],
    }),

    // PATCH /api/seller/orders/{id}/status
    updateOrderStatus: builder.mutation({
      query: ({ id, status }) => ({
        url: `/seller/orders/${id}/status`,
        method: "PATCH",
        body: { status },
      }),
      invalidatesTags: ["Orders"],
    }),

    // DELETE /api/seller/orders/{id}
    deleteOrder: builder.mutation({
      query: (id) => ({
        url: `/seller/orders/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Orders"],
    }),

    getRevenue: builder.query<any, void>({
      query: () => "/seller/orders/revenue",
    }),

    getTotalRevenue: builder.query<any, void>({
      query: () => "/seller/orders/revenue/total",
    }),

    getCompletedOrders: builder.query<any, void>({
      query: () => "/seller/orders/completed",
    }),
  }),
});

export const {
  useGetOrdersQuery,
  useGetOrderByIdQuery,
  useUpdateOrderStatusMutation,
  useDeleteOrderMutation,
  useGetRevenueQuery,
  useGetTotalRevenueQuery,
  useGetCompletedOrdersQuery,
} = orderApi;