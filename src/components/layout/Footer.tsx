import Link from "next/link";

const footerLinks = {
  考试频道: [
    { name: "国家公务员考试", href: "/guokao" },
    { name: "各省公务员考试", href: "/shengkao" },
    { name: "上海社区工作者", href: "/shanghai-shegong" },
  ],
  备考资源: [
    { name: "报考公告", href: "/baokao-gonggao" },
    { name: "政策解读", href: "/zhengce-jiedu" },
    { name: "备考指南", href: "/beikao-zhinan" },
    { name: "真题解析", href: "/zhenti-jiexi" },
  ],
  更多: [
    { name: "岗位分析", href: "/gangwei-fenxi" },
    { name: "上岸经验", href: "/shang-an-jingyan" },
  ],
};

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {/* 品牌信息 */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <span className="text-2xl">🏛️</span>
              <span className="text-lg font-bold text-white">公考资讯站</span>
            </Link>
            <p className="text-sm text-gray-400 leading-relaxed">
              专注国考、省考、社区工作者招录考试，提供最新招考公告与备考指南，助你顺利上岸。
            </p>
          </div>

          {/* 链接区 */}
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h3 className="text-white font-semibold mb-4">{title}</h3>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-gray-400 hover:text-white transition-colors"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* 版权 */}
        <div className="border-t border-gray-800 mt-10 pt-6 text-center text-sm text-gray-500">
          <p>© {new Date().getFullYear()} 公考资讯站. 仅供学习交流，不构成报考建议。</p>
        </div>
      </div>
    </footer>
  );
}
