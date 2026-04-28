import Link from "next/link";
import type { Metadata } from "next";
import { getAllArticles, categories, getCategoryCount } from "@/lib/content";

export const metadata: Metadata = {
  alternates: {
    canonical: "https://gk.edu-sjtu.cn",
  },
  twitter: {
    card: "summary_large_image",
    title: "公考资讯站 - 国考省考社区工作者招录公告与备考指南",
    description: "专注国考、省考、上海社区工作者招录考试，提供最新招考公告、政策解读、备考指南、真题解析与上岸经验分享。",
  },
};

// 热搜关键词 → 指向真实分类/内容页
const hotKeywords = [
  { label: "2026国考时间", href: "/guokao" },
  { label: "国考职位表", href: "/gangwei-fenxi" },
  { label: "省考报名条件", href: "/baokao-gonggao" },
  { label: "上海社区工作者招聘", href: "/shanghai-shegong" },
  { label: "行测备考攻略", href: "/beikao-zhinan" },
  { label: "申论范文", href: "/zhenti-jiexi" },
  { label: "面试技巧", href: "/shang-an-jingyan" },
  { label: "公务员薪资待遇", href: "/gangwei-fenxi" },
  { label: "社区工作者考试内容", href: "/shanghai-shegong" },
  { label: "国考真题解析", href: "/zhenti-jiexi" },
  { label: "应届生考公指南", href: "/zhengce-jiedu" },
  { label: "公务员体检标准", href: "/zhengce-jiedu" },
];

export default function HomePage() {
  const allArticles = getAllArticles();
  const categoryCounts = getCategoryCount();
  const latestArticles = allArticles.slice(0, 8);

  return (
    <>
      {/* Hero 区域 */}
      <section className="bg-gradient-to-br from-blue-800 via-blue-700 to-indigo-800 text-white">
        <div className="max-w-6xl mx-auto px-4 py-16 md:py-24">
          <h1 className="text-3xl md:text-5xl font-bold mb-4">
            🏛️ 公考资讯站
          </h1>
          <p className="text-lg md:text-xl text-blue-100 mb-8 max-w-2xl">
            专注国考、省考、上海社区工作者招录考试。最新公告、备考指南、真题解析，助你一战上岸。
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/baokao-gonggao"
              className="bg-white text-blue-800 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition"
            >
              📢 查看最新公告
            </Link>
            <Link
              href="/beikao-zhinan"
              className="border border-white/30 text-white px-6 py-3 rounded-lg font-medium hover:bg-white/10 transition"
            >
              📚 备考指南
            </Link>
          </div>
        </div>
      </section>

      {/* 频道分类 */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          📂 考试频道
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.slug}
              href={`/${cat.slug}`}
              className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-200 transition-all group"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-700">
                  {cat.name}
                </h3>
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                  {categoryCounts[cat.slug] || 0} 篇
                </span>
              </div>
              <p className="text-sm text-gray-500">{cat.description}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* 最新文章 */}
      <section className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            📰 最新资讯
          </h2>
          <Link
            href="/baokao-gonggao"
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            查看全部 →
          </Link>
        </div>
        {latestArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {latestArticles.map((article, idx) => (
              <Link
                key={article.slug}
                href={`/${article.category}/${article.slug}`}
                className={`bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all ${
                  idx === 0 ? "md:col-span-2 md:flex md:gap-6" : ""
                }`}
              >
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-medium">
                      {categories.find((c) => c.slug === article.category)?.name || article.category}
                    </span>
                    <span className="text-xs text-gray-400">
                      {article.date}
                    </span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                    {article.title}
                  </h3>
                  <p className="text-sm text-gray-500 line-clamp-2">
                    {article.description}
                  </p>
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
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-xl p-12 text-center border border-gray-100">
            <p className="text-4xl mb-4">📝</p>
            <p className="text-gray-500">网站正在建设中，敬请期待...</p>
            <p className="text-sm text-gray-400 mt-2">
              自动化内容发布即将上线，届时每日更新公考资讯
            </p>
          </div>
        )}
      </section>

      {/* SEO 内容区 - 关键词聚合 */}
      <section className="bg-white border-t border-gray-100">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            🔍 公考热门搜索
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {hotKeywords.map((kw) => (
              <Link
                key={kw.label}
                href={kw.href}
                className="text-sm text-gray-600 bg-gray-50 hover:bg-blue-50 hover:text-blue-700 px-3 py-2 rounded-lg transition"
              >
                🔎 {kw.label}
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
