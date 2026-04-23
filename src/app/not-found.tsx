import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-24 text-center">
      <p className="text-6xl mb-4">🔍</p>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">页面未找到</h1>
      <p className="text-gray-500 mb-8">
        您访问的页面不存在或已被移除。
      </p>
      <Link
        href="/"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
      >
        返回首页
      </Link>
    </div>
  );
}
