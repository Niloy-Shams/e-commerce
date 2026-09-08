export interface Category {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  image_url: string | null;
  category_id: number;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

export interface PaginatedProducts {
  items: Product[];
  page: number;
  limit: number;
  total: number;
  pages: number;
}

export type ProductSort = "price_asc" | "price_desc" | "newest" | "name_asc" | "name_desc";
