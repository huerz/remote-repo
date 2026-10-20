// ============================================================================
// 全局类型定义：与后端数据表 / 接口返回结构一一对应
// 说明：TypeScript 的类型只在开发期存在，编译后会被全部擦除，不影响运行结果
// ============================================================================

// 文学作品类型（对应后端 classictype 表 / GET /api/classics/get-classictypes）
export interface Classictype {
  tid: number
  name: string
  cover: string | null
  remark: string | null
}

// 文学作品（对应后端 classics 表 / POST /api/classics/search-classics）
export interface Classic {
  cid: number
  title: string
  tid: number
  cover: string | null
  year: string | null
  author: string | null
  present: string | null
  describes: string | null
  rating: number | null
  commentscount: number | null
}

// 后端统一返回结构：{ code, msg, data }
export interface ApiResult<T> {
  code: string
  msg: string
  data: T
}

// 首页推荐区按类型分组后的结构
export interface RecommendGroup {
  tid: number
  name: string
  list: Classic[]
}
