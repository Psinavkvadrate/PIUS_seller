import { baseApi } from "../../../shared/api/baseApi";

export const orderApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getOrders: builder.query({
      query: (params) => ({
        url: "/seller/orders",
        params,
      }),
      providesTags: ["Orders"],
    }),

    getOrderById: builder.query({
      query: (id) => ({
        url: `/seller/orders/${id}`,
      }),
      providesTags: (result, error, id) => [{ type: "Orders", id }],
    }),

    updateOrderStatus: builder.mutation({
      query: ({ id, status }) => ({
        url: `/seller/orders/${id}/status`,
        method: "PATCH",
        body: { status },
      }),
      invalidatesTags: (result, error, { id }) => [
        "Orders",
        { type: "Orders", id },
      ],
    }),

    deleteOrder: builder.mutation({
      query: (id) => ({
        url: `/seller/orders/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Orders"],
    }),
  }),
});

export const {
  useGetOrdersQuery,
  useGetOrderByIdQuery,
  useUpdateOrderStatusMutation,
  useDeleteOrderMutation,
} = orderApi;