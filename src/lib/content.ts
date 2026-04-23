import fs from "fs";
import path from "path";
import matter from "gray-matter";
import readingTime from "reading-time";
import type { ArticleMeta, ArticleData, CategoryInfo } from "./types";

const contentDir = path.join(process.cwd(), "content");

// 频道分类配置
export const categories: CategoryInfo[] = [
  {
    name: "国考",
    slug: "guokao",
    description: "国家公务员考试招录公告、职位表、政策解读与备考指南",
    keywords: ["国考", "国家公务员考试", "国考公告", "国考职位表", "国考时间"],
  },
  {
    name: "省考",
    slug: "shengkao",
    description: "各省市公务员考试信息汇总，含多省联考和独立省考",
    keywords: ["省考", "省考公告", "省考时间", "多省联考", "省考职位表"],
  },
  {
    name: "上海社区工作者",
    slug: "shanghai-shegong",
    description: "上海社区工作者招聘公告、考试信息、政策待遇与备考资料",
    keywords: [
      "上海社区工作者",
      "上海社工",
      "上海社区工作者招聘",
      "上海社工考试",
    ],
  },
  {
    name: "报考公告",
    slug: "baokao-gonggao",
    description: "各类公职考试报名公告、时间节点、岗位信息汇总",
    keywords: ["招考公告", "报名入口", "考试时间", "职位表", "报名条件"],
  },
  {
    name: "政策解读",
    slug: "zhengce-jiedu",
    description: "公务员考试政策变化、新规解读与趋势分析",
    keywords: ["政策解读", "考试政策", "报考条件", "新规变化"],
  },
  {
    name: "备考指南",
    slug: "beikao-zhinan",
    description: "行测、申论、面试备考方法、学习计划与复习攻略",
    keywords: ["备考指南", "行测", "申论", "面试", "复习计划"],
  },
  {
    name: "真题解析",
    slug: "zhenti-jiexi",
    description: "历年国考省考真题解析与答题技巧",
    keywords: ["真题", "真题解析", "历年真题", "真题答案"],
  },
  {
    name: "岗位分析",
    slug: "gangwei-fenxi",
    description: "热门岗位分析、薪资待遇对比、职业发展路径",
    keywords: ["岗位分析", "岗位待遇", "热门岗位", "报考指导"],
  },
  {
    name: "上岸经验",
    slug: "shang-an-jingyan",
    description: "公考上岸学员分享备考经验与心得",
    keywords: ["上岸经验", "备考心得", "经验分享", "高分经验"],
  },
];

// 获取所有文章的元数据
export function getAllArticles(): ArticleMeta[] {
  if (!fs.existsSync(contentDir)) return [];

  const articles: ArticleMeta[] = [];

  function walkDir(dir: string, category: string) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walkDir(fullPath, category || file);
      } else if (file.endsWith(".mdx") || file.endsWith(".md")) {
        const fileContent = fs.readFileSync(fullPath, "utf-8");
        const { data } = matter(fileContent);
        if (data.title) {
          articles.push({
            title: data.title || "",
            description: data.description || "",
            date: data.date ? String(data.date) : "",
            category: data.category || category || "",
            tags: data.tags || [],
            slug: file.replace(/\.(mdx|md)$/, ""),
            author: data.author || "公考资讯站",
            coverImage: data.coverImage || "",
          });
        }
      }
    }
  }

  walkDir(contentDir, "");

  // 按日期倒序排列
  articles.sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  return articles;
}

// 获取单篇文章完整数据
export function getArticleBySlug(
  slug: string,
  category?: string
): ArticleData | null {
  // 搜索范围：指定分类目录 或 全部
  const searchDirs: string[] = [];
  if (category) {
    searchDirs.push(path.join(contentDir, category));
  }
  searchDirs.push(contentDir);

  for (const dir of searchDirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir);
    for (const file of files) {
      if (file === `${slug}.mdx` || file === `${slug}.md`) {
        const fullPath = path.join(dir, file);
        const fileContent = fs.readFileSync(fullPath, "utf-8");
        const { data, content } = matter(fileContent);
        const time = readingTime(content);

        return {
          title: data.title || "",
          description: data.description || "",
          date: data.date ? String(data.date) : "",
          category: data.category || category || "",
          tags: data.tags || [],
          slug,
          author: data.author || "公考资讯站",
          coverImage: data.coverImage || "",
          content,
          readingTime: time.text,
        };
      }
    }
  }

  return null;
}

// 按分类获取文章
export function getArticlesByCategory(category: string): ArticleMeta[] {
  return getAllArticles().filter(
    (a) => a.category.toLowerCase() === category.toLowerCase()
  );
}

// 获取相关文章
export function getRelatedArticles(
  currentSlug: string,
  currentCategory: string,
  limit = 5
): ArticleMeta[] {
  return getAllArticles()
    .filter(
      (a) => a.slug !== currentSlug && a.category === currentCategory
    )
    .slice(0, limit);
}

// 获取所有分类下的文章数量
export function getCategoryCount(): Record<string, number> {
  const articles = getAllArticles();
  const counts: Record<string, number> = {};
  for (const a of articles) {
    counts[a.category] = (counts[a.category] || 0) + 1;
  }
  return counts;
}
