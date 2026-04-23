import Link from "next/link";

const navItems = [
  { name: "国考", href: "/guokao" },
  { name: "省考", href: "/shengkao" },
  { name: "上海社工", href: "/shanghai-shegong" },
  { name: "公告", href: "/baokao-gonggao" },
  { name: "备考", href: "/beikao-zhinan" },
  { name: "真题", href: "/zhenti-jiexi" },
  { name: "经验", href: "/shang-an-jingyan" },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 shrink-0">
            <span className="text-2xl">🏛️</span>
            <span className="text-xl font-bold text-blue-800 hidden sm:inline">
              公考资讯站
            </span>
          </Link>

          {/* 导航 */}
          <nav className="flex items-center gap-1 overflow-x-auto">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors whitespace-nowrap"
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
