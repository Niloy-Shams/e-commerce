import { create } from "zustand";

export interface CartItem {
  product_id: number;
  name: string;
  price: number;
  image_url: string | null;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: number) => void;
  increaseQuantity: (productId: number) => void;
  decreaseQuantity: (productId: number) => void;
  clearCart: () => void;
  subtotal: () => number;
  itemCount: () => number;
}

// The cart here is NOT authoritative for price or stock (section 20).
// At checkout, the backend must re-read product price/stock from the DB.
export const useCartStore = create<CartState>((set, get) => ({
  items: [],

  addItem: (item) =>
    set((state) => {
      const existing = state.items.find((i) => i.product_id === item.product_id);
      if (existing) {
        return {
          items: state.items.map((i) =>
            i.product_id === item.product_id ? { ...i, quantity: i.quantity + item.quantity } : i
          ),
        };
      }
      return { items: [...state.items, item] };
    }),

  removeItem: (productId) =>
    set((state) => ({ items: state.items.filter((i) => i.product_id !== productId) })),

  increaseQuantity: (productId) =>
    set((state) => ({
      items: state.items.map((i) =>
        i.product_id === productId ? { ...i, quantity: i.quantity + 1 } : i
      ),
    })),

  decreaseQuantity: (productId) =>
    set((state) => ({
      items: state.items
        .map((i) => (i.product_id === productId ? { ...i, quantity: i.quantity - 1 } : i))
        .filter((i) => i.quantity > 0),
    })),

  clearCart: () => set({ items: [] }),

  subtotal: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),

  itemCount: () => get().items.reduce((sum, i) => sum + i.quantity, 0),
}));
