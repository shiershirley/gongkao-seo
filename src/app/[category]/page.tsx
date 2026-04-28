import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { categories, getArticlesByCategory } from "@/lib/content";
import { Breadcrumbs } from "@/components/ui/Breadcrumbs";
import { ArticleCard } from "@/components/ui/ArticleCard";

interface PageProps {
  params: Promise<{ category: string }>;
}

// 生成所有分类的静态路径
export async function generateStaticParams() {
  return categories.map((cat) => ({ category: cat.slug }));
}

// 动态生成 metadata
export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { category } = await params;
  const cat = categories.find((c) => c.slug === category);
  if (!cat) return {};

  const canonicalUrl = `https://gk.edu-sjtu.cn/${category}`;

  return {
    title: `${cat.name} - ${cat.description}`,
    description: cat.description,
    keywords: cat.keywords,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title: `${cat.name} | 公考资讯站`,
      description: cat.description,
      url: canonicalUrl,
    },
    twitter: {
      card: "summary",
      title: `${cat.name} | 公考资讯站`,
      description: cat.description,
    },
  };
}

export default async function CategoryPage({ params }: PageProps) {
  const { category } = await params;
  const cat = categories.find((c) => c.slug === category);

  if (!cat) notFound();

  const articles = getArticlesByCategory(category);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <Breadcrumbs items={[{ label: cat.name }]} />

      {/* 分类头部 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{cat.name}</h1>
        <p className="text-gray-500">{cat.description}</p>
        <div className="flex gap-2 mt-4 flex-wrap">
          {cat.keywords.map((kw) => (
            <span
              key={kw}
              className="text-xs bg-blue-50 text-blue-600 px-3 py-1 rounded-full"
            >
              {kw}
            </span>
          ))}
        </div>
      </div>

      {/* 文章列表 */}
      {articles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {articles.map((article) => (
            <ArticleCard key={article.slug} article={article} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-xl p-12 text-center border border-gray-100">
          <p className="text-4xl mb-4">📝</p>
          <p className="text-gray-500">该分类暂无文章</p>
          <p className="text-sm text-gray-400 mt-2">
            自动化内容发布即将上线，敬请期待
          </p>
          <Link
            href="/"
            className="inline-block mt-4 text-blue-600 hover:text-blue-800 text-sm"
          >
            ← 返回首页
          </Link>
        </div>
      )}
    </div>
  );
}
