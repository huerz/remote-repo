// ============================================================================
// 页面缩放锁
// ----------------------------------------------------------------------------
// 作用：按项目规则禁止任意缩放页面大小（含 Ctrl + 鼠标滚轮），保证布局尺寸恒定。
// 用法：在 main.ts 挂载应用前调用一次 installZoomLock()。
// 约定：本规则只挡页面缩放，不影响正常滚动与键盘输入，见下方逐条说明。
// 撤销：注释掉 main.ts 里的调用即可，不需要改动本文件。
// ============================================================================
/** 需要拦截的缩放按键（含小键盘加号与主键盘等号、下划线） */
const ZOOM_KEYS = ['+', '-', '=', '_', '0'];
/** 只允许横向纵向平移，禁掉触屏双指缩放 */
const TOUCH_ACTION = 'pan-x pan-y';
/** Safari 的捏合手势事件名（Chrome / Firefox 不会触发） */
const GESTURE_EVENTS = ['gesturestart', 'gesturechange', 'gestureend'];
/**
 * 安装页面缩放锁。
 *
 * 拦住三类入口：
 *   1) Ctrl / ⌘ + 滚轮——鼠标滚轮缩放；触控板双指捏合浏览器也会伪装成带 ctrlKey
 *      的 wheel 事件，所以一并挡掉（必须 passive: false 才允许 preventDefault）
 *   2) Ctrl / ⌘ + 「+」「-」「=」「0」——键盘缩放与复位
 *   3) 双指捏合——CSS touch-action 限制 + Safari 的 gesture 事件兜底
 *
 * 注意：浏览器菜单里的「缩放」属于浏览器级操作，JS 拦不住，只能挡常用入口。
 *
 * @returns 无返回值；重复调用会重复绑定监听器，只应在应用入口调用一次。
 */
export function installZoomLock() {
    window.addEventListener(// 1. Ctrl / ⌘ + 滚轮
    'wheel', function (event) {
        if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
        }
    }, { passive: false });
    window.addEventListener('keydown', function (event) {
        if (!(event.ctrlKey || event.metaKey))
            return;
        if (ZOOM_KEYS.includes(event.key)) {
            event.preventDefault();
        }
    });
    GESTURE_EVENTS.forEach(function (name) {
        window.addEventListener(name, function (event) {
            event.preventDefault();
        }, { passive: false });
    });
    document.documentElement.style.touchAction = TOUCH_ACTION; // 4. 触屏双指缩放：只允许横向纵向平移
}
