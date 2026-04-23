import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL("https://gongkao.example.com"),
  title: {
    default: "公考资讯站 - 国考省考社区工作者招录公告与备考指南",
    template: "%s | 公考资讯站",
  },
  description:
    "专注国考、省考、上海社区工作者招录考试，提供最新招考公告、政策解读、备考指南、真题解析与上岸经验分享。",
  keywords: [
    "公务员考试",
    "国考",
    "省考",
    "上海社区工作者",
    "招考公告",
    "备考指南",
    "行测",
    "申论",
  ],
  openGraph: {
    type: "website",
    locale: "zh_CN",
    siteName: "公考资讯站",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={`${inter.className} antialiased`}>
        <Header />
        <main className="min-h-screen bg-gray-50">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
