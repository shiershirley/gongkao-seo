export interface ArticleMeta {
  title: string;
  description: string;
  date: string;
  category: string;
  tags: string[];
  slug: string;
  author?: string;
  coverImage?: string;
}

export interface ArticleData extends ArticleMeta {
  content: string;
  readingTime: string;
}

export interface CategoryInfo {
  name: string;
  slug: string;
  description: string;
  keywords: string[];
}
