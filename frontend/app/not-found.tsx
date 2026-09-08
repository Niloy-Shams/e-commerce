import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <h1 className="text-xl font-semibold text-gray-900">Page not found</h1>
      <p className="mt-2 text-gray-600">The page you&apos;re looking for doesn&apos;t exist.</p>
      <Link href="/" className="mt-6 text-sm font-medium text-gray-900 underline">
        Back to home
      </Link>
    </div>
  );
}
