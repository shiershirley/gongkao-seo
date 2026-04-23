import Link from "next/link";
import type { ArticleMeta } from "@/lib/types";
import { categories } from "@/lib/content";

export function ArticleCard({ article }: { article: ArticleMeta }) {
  const cat = categories.find((c) => c.slug === article.category);

  return (
    <Link
      href={`/${article.category}/${article.slug}`}
      className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all group block"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
          {cat?.name || article.category}
        </span>
        <time className="text-xs text-gray-400">{article.date}</time>
      </div>
      <h3 className="font-semibold text-gray-900 mb-1 group-hover:text-blue-700 transition-colors line-clamp-2">
        {article.title}
      </h3>
      <p className="text-sm text-gray-500 line-clamp-2">{article.description}</p>
      {article.tags.length > 0 && (
        <div className="flex gap-1 mt-3 flex-wrap">
          {article.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}
