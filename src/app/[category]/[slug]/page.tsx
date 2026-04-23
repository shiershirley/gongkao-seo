import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { categories, getArticleBySlug, getRelatedArticles } from "@/lib/content";
import { Breadcrumbs } from "@/components/ui/Breadcrumbs";

interface PageProps {
  params: Promise<{ category: string; slug: string }>;
}

// 动态生成 metadata
export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { category, slug } = await params;
  const article = getArticleBySlug(slug, category);
  if (!article) return {};

  return {
    title: article.title,
    description: article.description,
    keywords: article.tags,
    openGraph: {
      title: article.title,
      description: article.description,
      type: "article",
      publishedTime: article.date,
      authors: [article.author || "公考资讯站"],
    },
  };
}

export default async function ArticlePage({ params }: PageProps) {
  const { category, slug } = await params;
  const article = getArticleBySlug(slug, category);

  if (!article) notFound();

  const cat = categories.find((c) => c.slug === article.category);
  const relatedArticles = getRelatedArticles(slug, article.category, 4);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Breadcrumbs
        items={[
          { label: cat?.name || article.category, href: `/${article.category}` },
          { label: article.title },
        ]}
      />

      {/* 文章头部 */}
      <article>
        <header className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
              {cat?.name || article.category}
            </span>
            <time className="text-sm text-gray-400">{article.date}</time>
            <span className="text-sm text-gray-400">{article.readingTime}</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">
            {article.title}
          </h1>
          <p className="text-lg text-gray-500">{article.description}</p>
          {article.tags.length > 0 && (
            <div className="flex gap-2 mt-4 flex-wrap">
              {article.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-sm bg-gray-100 text-gray-500 px-3 py-1 rounded-full"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </header>

        {/* 文章内容（MDX 渲染由 gray-matter 提取 content 字段） */}
        <div
          className="prose max-w-none"
          dangerouslySetInnerHTML={{
            __html: renderMarkdownToHtml(article.content),
          }}
        />

        {/* 底部信息 */}
        <footer className="mt-12 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-400">
              作者：{article.author} | 发布：{article.date}
            </p>
            <Link
              href={`/${article.category}`}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              ← 返回{cat?.name || article.category}
            </Link>
          </div>
        </footer>
      </article>

      {/* 相关文章 */}
      {relatedArticles.length > 0 && (
        <aside className="mt-12">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            📖 相关推荐
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {relatedArticles.map((rel) => (
              <Link
                key={rel.slug}
                href={`/${rel.category}/${rel.slug}`}
                className="bg-white p-4 rounded-lg border border-gray-100 hover:shadow-sm transition"
              >
                <h3 className="font-medium text-gray-900 text-sm line-clamp-2 mb-1">
                  {rel.title}
                </h3>
                <p className="text-xs text-gray-400">{rel.date}</p>
              </Link>
            ))}
          </div>
        </aside>
      )}
    </div>
  );
}

// 简单的 Markdown → HTML 转换
function renderMarkdownToHtml(markdown: string): string {
  const lines = markdown.split('\n');
  const result: string[] = [];
  let inList = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // 标题
    if (/^### /.test(trimmed)) {
      if (inList) { result.push('</ul>'); inList = false; }
      result.push(`<h3>${processInline(trimmed.slice(4))}</h3>`);
    } else if (/^## /.test(trimmed)) {
      if (inList) { result.push('</ul>'); inList = false; }
      result.push(`<h2>${processInline(trimmed.slice(3))}</h2>`);
    } else if (/^# /.test(trimmed)) {
      if (inList) { result.push('</ul>'); inList = false; }
      result.push(`<h1>${processInline(trimmed.slice(2))}</h1>`);
    }
    // 引用
    else if (/^> /.test(trimmed)) {
      if (inList) { result.push('</ul>'); inList = false; }
      result.push(`<blockquote>${processInline(trimmed.slice(2))}</blockquote>`);
    }
    // 无序列表
    else if (/^- /.test(trimmed)) {
      if (!inList) { result.push('<ul>'); inList = true; }
      result.push(`<li>${processInline(trimmed.slice(2))}</li>`);
    }
    // 空行
    else if (trimmed === '') {
      if (inList) { result.push('</ul>'); inList = false; }
    }
    // 普通段落
    else {
      if (inList) { result.push('</ul>'); inList = false; }
      result.push(`<p>${processInline(trimmed)}</p>`);
    }
  }

  if (inList) result.push('</ul>');
  return result.join('\n');
}

function processInline(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}
