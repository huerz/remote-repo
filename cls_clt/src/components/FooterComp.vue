<template>
  <div class="footer-comp">
    <span class="footer-links">关于我们 | 招贤纳士 | 商务合作 | 在线客服</span>
    <span class="footer-time">工作时间 8:30-22:00</span>
  </div>
</template>

<style scoped>
.footer-comp {
  line-height: 60px;
  color: #606266;
  font-size: 14px;
  white-space: nowrap;
}

.footer-time {
  margin-left: 6px;
}

/* 手机屏幕放不下一整行（约需 420px）：允许在两组文案之间换行并压小字号，
   时间单独一段且不许拆行，否则会出现「8:30- / 22:00」这种断法 */
@media (max-width: 760px) {
  .footer-comp {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    column-gap: 10px;
    padding: 12px 8px;
    font-size: 12px;
    line-height: 1.8;
    white-space: normal;
  }

  .footer-time {
    margin-left: 0;
    white-space: nowrap;
  }
}
</style>
