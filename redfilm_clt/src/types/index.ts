// ============================================================================
// 全局类型定义：与后端数据表 / 接口返回结构一一对应
// 说明：TypeScript 的类型只在开发期存在，编译后会被全部擦除，不影响运行结果
// ============================================================================

// 电影类型（对应后端 filmtype 表 / GET /api/films/get-filmtypes）
export interface Filmtype {
  tid: number
  name: string
  cover: string | null
  remark: string | null
}

// 电影（对应后端 films 表 / POST /api/films/search-films）
export interface Film {
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

// 评论用户（后端 UsersSchema 序列化结果，注意不含密码字段）
export interface DiscussUser {
  uid: number
  uname: string
  nickname: string | null
  avatar: string | null
  sex: string | null
  phone: string | null
  remark: string | null
}

// 电影影评（对应后端 discuss 表 / GET /api/films/get-discuss/<cid>）
// cdate 后端统一格式化为 "YYYY-MM-DD HH:MM"
export interface Discuss {
  did: number
  cid: number
  comment: string | null
  cdate: string | null
  topcount: number | null
  lowcount: number | null
  user: DiscussUser
}

// 首页推荐区结构：GET /api/films/recommend-films/<n> 返回的分组
// 每一项是一个电影类型 + 该类型下评分最高的若干部影片
export interface RecommendGroup {
  tid: number
  name: string
  cover: string | null
  remark: string | null
  films: Film[]
}
