export type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "PROCESSING"
  | "SHIPPED"
  | "DELIVERED"
  | "CANCELLED";

export interface OrderItem {
  product_id: number;
  name: string;
  quantity: number;
  price: number;
}

export interface Order {
  id: string;
  user_id: string;
  total_amount: number;
  shipping_name: string;
  shipping_phone: string;
  shipping_address: string;
  status: OrderStatus;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface OrderItemInput {
  product_id: number;
  quantity: number;
}

export interface OrderCreateInput {
  items: OrderItemInput[];
  shipping_name: string;
  shipping_phone: string;
  shipping_address: string;
}
