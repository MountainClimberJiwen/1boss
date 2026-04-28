<template>
  <div class="page-shell">
    <div class="hero-wrap">
      <header class="hero-header">
        <div class="hero-logo">
          <img class="hero-logo-img" src="/logo.png" alt="1boss logo" />
          <span>1boss</span>
        </div>
        <nav class="hero-nav"><a>产品</a><a>文档</a><a>定价</a></nav>
        <div class="hero-actions"><button class="btn small">登录</button><button class="btn light small">立即开始</button><RouterLink class="btn small" to="/website/en">EN</RouterLink></div>
      </header>

      <section class="hero-main">
        <div>
          <h1 class="title">一个老板，一支军团</h1>
          <p class="section-sub">将项目推进、任务节奏和想法沉淀放在同一个技术型工作台，专注推进交付。</p>
          <div class="hero-actions"><button class="btn light">免费开始</button><button class="btn">预约演示</button></div>
        </div>
        <div class="hero-panel">
          <div style="font-weight:600;margin-bottom:8px;">运行看板</div>
          <table class="table"><thead><tr><th>T2</th><th>42</th><th>18</th></tr></thead><tbody><tr><td>任务合并</td><td>运行中</td><td>10秒</td></tr><tr><td>想法同步</td><td>排队中</td><td>04秒</td></tr></tbody></table>
        </div>
      </section>

      <section class="hero-panel" style="margin-bottom:12px;"><div style="font-weight:600;margin-bottom:10px;">为独立开发者打造的核心能力</div><div class="grid-3"><div class="card"><div class="kpi-label">快速捕捉想法</div><p class="section-sub">把灵感直接变成可执行任务，避免中断流失。</p></div><div class="card"><div class="kpi-label">拆解复杂工作</div><p class="section-sub">将大任务拆解为明确步骤、验收标准和负责人。</p></div><div class="card"><div class="kpi-label">以短迭代交付</div><p class="section-sub">通过短周期推进，持续可见地输出结果。</p></div></div></section>

      <section class="hero-panel" style="margin-bottom:12px;"><div style="font-weight:600;margin-bottom:10px;">1boss 的实际工作方式</div><div class="grid-3"><div class="card"><div class="kpi-label">01. 收集</div><div class="section-title" style="font-size:20px;">收件箱</div></div><div class="card"><div class="kpi-label">02. 规划</div><div class="section-title" style="font-size:20px;">列表</div></div><div class="card"><div class="kpi-label">03. 交付</div><div class="section-title" style="font-size:20px;">发布</div></div></div></section>

      <section class="hero-panel"><div style="font-weight:600;margin-bottom:10px;">独立开发者的数据反馈</div><div class="grid-4"><div class="card"><div class="kpi-label">规划耗时</div><div class="section-title" style="font-size:24px;">-38%</div></div><div class="card"><div class="kpi-label">任务完成量</div><div class="section-title" style="font-size:24px;">+2.4x</div></div><div class="card"><div class="kpi-label">想法到任务延迟</div><div class="section-title" style="font-size:24px;">&lt;12h</div></div><div class="card"><div class="kpi-label">专注保持率</div><div class="section-title" style="font-size:24px;">91%</div></div></div></section>
    </div>
  </div>
</template>
