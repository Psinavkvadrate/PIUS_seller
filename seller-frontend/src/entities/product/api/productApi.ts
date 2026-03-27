import { baseApi } from "../../../shared/api/baseApi";

export const productApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getMyProducts: builder.query({
      query: (params) => ({
        url: "/products/my",
        params,
      }),
      providesTags: ["Products"],
    }),

    createProduct: builder.mutation({
      query: (body) => ({
        url: "/products",
        method: "POST",
        body,
      }),
      invalidatesTags: ["Products"],
    }),

    updateProduct: builder.mutation({
      query: ({ id, ...body }) => ({
        url: `/products/${id}`,
        method: "PATCH",
        body,
      }),
      invalidatesTags: ["Products"],
    }),

    deleteProduct: builder.mutation({
      query: (id) => ({
        url: `/products/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["Products"],
    }),
  }),
});

export const {
  useGetMyProductsQuery,
  useCreateProductMutation,
  useUpdateProductMutation,
  useDeleteProductMutation,
} = productApi;
