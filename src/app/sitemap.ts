import { MetadataRoute } from "next";
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { categories } from "@/lib/content";

const contentDir = path.join(process.cwd(), "content");

// 从文件名提取 slug（去掉日期前缀和 .md 后缀）
function extractSlug(filename: string): string {
  // 移除 .md 或 .mdx 扩展名
  const withoutExt = filename.replace(/\.(mdx|md)$/, "");
  return withoutExt;
}

// 从文件路径推断 category
function inferCategory(filePath: string): string {
  const relative = path.relative(contentDir, filePath);
  const parts = relative.split(path.sep);
  // 如果文件在子目录中，子目录名就是 category
  if (parts.length > 1) {
    return parts[0];
  }
  return "";
}

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://gk.edu-sjtu.cn";
  const now = new Date();

  // 静态页面
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: now,
      changeFrequency: "daily",
      priority: 1.0,
    },
    ...categories.map((cat) => ({
      url: `${baseUrl}/${cat.slug}`,
      lastModified: now,
      changeFrequency: "daily" as const,
      priority: 0.8,
    })),
  ];

  // 动态文章页 —— 直接从文件系统扫描，不依赖 getAllArticles
  // 这样即使 frontmatter 缺少 title，文章 URL 仍会出现在 Sitemap 中
  const articlePages: MetadataRoute.Sitemap = [];
  const seenSlugs = new Set<string>();

  function walkDir(dir: string) {
    if (!fs.existsSync(dir)) return;
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walkDir(fullPath);
      } else if (file.endsWith(".md") || file.endsWith(".mdx")) {
        try {
          const fileContent = fs.readFileSync(fullPath, "utf-8");
          const { data } = matter(fileContent);

          const slug = extractSlug(file);
          const category = data.category || inferCategory(fullPath) || "";
          const url = `${baseUrl}/${category}/${slug}`;

          // 避免重复 URL
          if (seenSlugs.has(url)) continue;
          seenSlugs.add(url);

          // 优先使用 frontmatter 中的 date，否则使用文件修改时间
          const lastMod = data.date ? new Date(data.date) : stat.mtime;

          articlePages.push({
            url,
            lastModified: lastMod,
            changeFrequency: "weekly" as const,
            priority: 0.6,
          });
        } catch {
          // 如果解析失败，仍然尝试生成 URL
          const slug = extractSlug(file);
          const category = inferCategory(fullPath) || "";
          const url = `${baseUrl}/${category}/${slug}`;
          if (!seenSlugs.has(url)) {
            seenSlugs.add(url);
            articlePages.push({
              url,
              lastModified: stat.mtime,
              changeFrequency: "weekly" as const,
              priority: 0.6,
            });
          }
        }
      }
    }
  }

  walkDir(contentDir);

  // 按 URL 排序，保持稳定的输出顺序
  articlePages.sort((a, b) => (a.url > b.url ? 1 : -1));

  return [...staticPages, ...articlePages];
}
