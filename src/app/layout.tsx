import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Script from "next/script";
import "./globals.css";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL("https://gk.edu-sjtu.cn"),
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
      <head>
        <meta name="baidu-site-verification" content="codeva-Uerc481wpT" />
        <meta name="google-site-verification" content="google_verification_code" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <Header />
        <main className="min-h-screen bg-gray-50">{children}</main>
        <Footer />
        {/* 百度统计 */}
        <Script
          id="baidu-tongji"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              var _hmt = _hmt || [];
              (function() {
                var hm = document.createElement("script");
                hm.src = "https://hm.baidu.com/hm.js?f7b8a430bf2c9a09bea0acdcf780c5b0";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(hm, s);
              })();
            `,
          }}
        />
        {/* 百度自动推送 */}
        <Script
          id="baidu-push"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              (function(){
                var bp = document.createElement('script');
                var curProtocol = window.location.protocol.split(':')[0];
                if (curProtocol === 'https') {
                  bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
                } else {
                  bp.src = 'http://push.zhanzhang.baidu.com/push.js';
                }
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(bp, s);
              })();
            `,
          }}
        />
      </body>
    </html>
  );
}
