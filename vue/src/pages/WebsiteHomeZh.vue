<template>
  <div class="page-shell">
    <div class="hero-wrap">
      <!-- Header -->
      <header class="hero-header fade-up">
        <div class="hero-logo">
          <img class="hero-logo-img" src="/logo.png" alt="1boss logo" />
          <span>1boss</span>
        </div>
        <nav class="hero-nav">
          <a href="#features">产品</a>
          <a href="#workflow">工作流</a>
          <a href="#proof">数据</a>
        </nav>
        <div class="hero-actions">
          <RouterLink class="btn small" to="/auth">登录</RouterLink>
          <button class="btn light small">立即开始</button>
          <RouterLink class="btn small" to="/website/en">EN</RouterLink>
        </div>
      </header>

      <!-- Hero -->
      <section class="hero-main" style="align-items:center;margin-bottom:32px;">
        <div class="fade-up stagger-1">
          <div class="eyebrow">专为独立开发者设计</div>
          <h1 class="title" style="font-size:52px;max-width:12ch;">一个老板<br />一支军团</h1>
          <p class="section-sub" style="font-size:14px;max-width:48ch;margin-top:16px;">
            将项目推进、任务节奏和想法沉淀放在同一个技术型工作台，专注推进交付。
          </p>
          <div class="hero-actions" style="margin-top:24px;">
            <button class="btn light">免费开始</button>
            <button class="btn">预约演示</button>
          </div>
        </div>
        <div class="hero-panel fade-up stagger-2" style="position:relative;">
          <div style="position:absolute;top:-40px;right:-20px;width:120px;height:120px;border-radius:999px;background:radial-gradient(circle,rgba(59,130,246,0.12),transparent 70%);filter:blur(40px);pointer-events:none;"></div>
          <div style="font-weight:700;margin-bottom:12px;font-size:14px;">运行看板</div>
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>任务</th>
                  <th>状态</th>
                  <th>耗时</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="font-weight:500;">任务合并</td>
                  <td>
                    <span style="display:inline-flex;align-items:center;gap:6px;">
                      <span class="unread-badge" style="width:6px;height:6px;margin:0;animation:none;background:#34d399;box-shadow:0 0 6px rgba(52,211,153,0.4);"></span>
                      运行中
                    </span>
                  </td>
                  <td class="mono">10s</td>
                </tr>
                <tr>
                  <td style="font-weight:500;">想法同步</td>
                  <td>
                    <span style="display:inline-flex;align-items:center;gap:6px;">
                      <span class="unread-badge" style="width:6px;height:6px;margin:0;animation:none;background:#fbbf24;box-shadow:0 0 6px rgba(251,191,36,0.4);"></span>
                      排队中
                    </span>
                  </td>
                  <td class="mono">04s</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- Features -->
      <section id="features" class="hero-panel fade-up stagger-3" style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:16px;align-items:center;">
          <div>
            <div class="eyebrow" style="margin-bottom:10px;">核心能力</div>
            <div style="font-weight:700;font-size:16px;">为独立开发者打造</div>
          </div>
        </div>
        <div class="grid-3">
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(56,189,248,0.15),rgba(56,189,248,0.05));border:1px solid rgba(56,189,248,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">快速捕捉想法</div>
            <p class="section-sub" style="margin:0;">把灵感直接变成可执行任务，避免中断流失。</p>
          </div>
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(167,139,250,0.15),rgba(167,139,250,0.05));border:1px solid rgba(167,139,250,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">拆解复杂工作</div>
            <p class="section-sub" style="margin:0;">将大任务拆解为明确步骤、验收标准和负责人。</p>
          </div>
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.05));border:1px solid rgba(52,211,153,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">以短迭代交付</div>
            <p class="section-sub" style="margin:0;">通过短周期推进，持续可见地输出结果。</p>
          </div>
        </div>
      </section>

      <!-- Workflow -->
      <section id="workflow" class="hero-panel fade-up stagger-4" style="margin-bottom:14px;">
        <div class="eyebrow" style="margin-bottom:10px;">工作流</div>
        <div style="font-weight:700;font-size:16px;margin-bottom:16px;">1boss 的实际工作方式</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">01. 收集</div>
            <div class="section-title" style="font-size:22px;margin:0;">收件箱</div>
            <p class="section-sub" style="margin:8px 0 0;">随时记录灵感，不遗漏任何想法。</p>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">02. 规划</div>
            <div class="section-title" style="font-size:22px;margin:0;">列表</div>
            <p class="section-sub" style="margin:8px 0 0;">将想法转化为可执行的任务清单。</p>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">03. 交付</div>
            <div class="section-title" style="font-size:22px;margin:0;">发布</div>
            <p class="section-sub" style="margin:8px 0 0;">按节奏推进，持续交付成果。</p>
          </div>
        </div>
      </section>

      <!-- Proof -->
      <section id="proof" class="hero-panel fade-up stagger-5">
        <div class="eyebrow" style="margin-bottom:10px;">数据反馈</div>
        <div style="font-weight:700;font-size:16px;margin-bottom:16px;">独立开发者的实际效果</div>
        <div class="grid-4">
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">规划耗时</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#34d399;">-38%</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">任务完成量</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#38bdf8;">+2.4x</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">想法到任务延迟</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#a78bfa;">&lt;12h</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">专注保持率</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#fbbf24;">91%</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
