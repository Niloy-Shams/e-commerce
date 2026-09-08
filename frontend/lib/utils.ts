/**
 * Merge conditional className strings, e.g.:
 *   cn("px-4 py-2", isActive && "bg-brand-primary", className)
 */
export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(" ");
}
