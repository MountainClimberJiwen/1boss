<template>
  <div class="page-shell">
    <!-- Aurora background -->
    <div class="aurora-bg">
      <div class="aurora-orb orb-1"></div>
      <div class="aurora-orb orb-2"></div>
      <div class="aurora-orb orb-3"></div>
      <div class="aurora-orb orb-4"></div>
    </div>
    <div class="hero-wrap" style="position:relative;z-index:1;">
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
          <a href="#integrate">集成</a>
        </nav>
        <div class="hero-actions">
          <RouterLink class="btn small" to="/auth">登录</RouterLink>
          <button class="btn light small">立即开始</button>
          <RouterLink class="btn small" to="/website/en">EN</RouterLink>
        </div>
      </header>

      <!-- Hero -->
      <section class="hero-main fade-up stagger-1" style="align-items:center;margin-bottom:80px;grid-template-columns:minmax(0,1fr) 480px;">
        <div>
          <div class="eyebrow" style="margin-bottom:20px;">专为独立开发者设计</div>
          <h1 class="hero-title-v2 gradient-text">一个老板<br />一支军团</h1>
          <p class="hero-desc-v2">
            将项目推进、任务节奏和想法沉淀放在同一个技术型工作台。专注推进交付，让一人团队也能拥有大厂的执行力。
          </p>
          <div class="hero-actions">
            <button class="btn light" style="padding:10px 20px;font-size:14px;">免费开始</button>
            <button class="btn" style="padding:10px 20px;font-size:14px;">预约演示</button>
          </div>
          <div style="display:flex;align-items:center;gap:20px;margin-top:28px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              永久免费起步
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              3 分钟完成配置
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              开源核心
            </div>
          </div>
        </div>

        <!-- Dashboard Mockup -->
        <div class="dashboard-mockup glow-border fade-up stagger-2" style="transform:rotate(1deg);">
          <div class="mockup-header">
            <div class="mockup-dot red"></div>
            <div class="mockup-dot yellow"></div>
            <div class="mockup-dot green"></div>
            <span style="margin-left:auto;font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);">1boss / dashboard</span>
          </div>
          <div class="mockup-content">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
              <span style="font-weight:700;font-size:13px;">运行看板</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);">Live</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status running"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">任务合并</span>
              <span style="font-size:11px;color:#34d399;font-family:var(--font-mono);">running</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">10s</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status queued"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">想法同步</span>
              <span style="font-size:11px;color:#fbbf24;font-family:var(--font-mono);">queued</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">04s</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status done"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">文档生成</span>
              <span style="font-size:11px;color:#38bdf8;font-family:var(--font-mono);">done</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">2m</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status running"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">依赖检查</span>
              <span style="font-size:11px;color:#34d399;font-family:var(--font-mono);">running</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">15s</span>
            </div>
            <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.04);display:flex;gap:12px;">
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#22d3ee;">12</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">活跃项目</div>
              </div>
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#a78bfa;">87%</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">本周完成</div>
              </div>
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#34d399;">3</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">待审想法</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Stats -->
      <section class="section-v2 fade-up stagger-2">
        <div class="stats-grid-v2">
          <div class="stat-item-v2">
            <div class="stat-value-v2 cyan">2,400+</div>
            <div class="stat-label-v2">独立开发者</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 purple">150K+</div>
            <div class="stat-label-v2">任务已完成</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 pink">12K+</div>
            <div class="stat-label-v2">想法被捕捉</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 amber">99.9%</div>
            <div class="stat-label-v2">运行稳定性</div>
          </div>
        </div>
      </section>

      <!-- Features -->
      <section id="features" class="section-v2 fade-up stagger-3">
        <div class="section-header-v2">
          <div class="eyebrow">核心能力</div>
          <h2 class="gradient-text">一人团队，全栈掌控</h2>
          <p>从灵感到交付的完整闭环，每个环节都为独立开发者优化</p>
        </div>
        <div class="feature-grid-v2">
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(34,211,238,0.15),rgba(34,211,238,0.05));border:1px solid rgba(34,211,238,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
            <h3>快速捕捉想法</h3>
            <p>把灵感直接变成可执行任务，避免中断流失。语音、速记、链接，任意方式记录。</p>
          </div>
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(167,139,250,0.15),rgba(167,139,250,0.05));border:1px solid rgba(167,139,250,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
            </div>
            <h3>拆解复杂工作</h3>
            <p>将大任务拆解为明确步骤、验收标准和负责人。AI 辅助估算工时与依赖关系。</p>
          </div>
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.05));border:1px solid rgba(52,211,153,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <h3>以短迭代交付</h3>
            <p>通过短周期推进，持续可见地输出结果。周报自动生成，进度一目了然。</p>
          </div>
        </div>
      </section>

      <!-- Code Integration -->
      <section id="integrate" class="section-v2 fade-up stagger-4">
        <div class="section-header-v2">
          <div class="eyebrow">即插即用</div>
          <h2 class="gradient-text">一行命令，即刻上线</h2>
          <p>无需改造现有工作流，3 分钟完成接入，开始追踪你的第一个项目</p>
        </div>
        <div class="code-block glow-border" style="max-width:720px;margin:0 auto;">
          <div class="code-block-header">
            <span style="display:flex;align-items:center;gap:8px;">
              <span class="mockup-dot red" style="width:8px;height:8px;"></span>
              <span class="mockup-dot yellow" style="width:8px;height:8px;"></span>
              <span class="mockup-dot green" style="width:8px;height:8px;"></span>
            </span>
            <span style="font-family:var(--font-mono);">terminal</span>
          </div>
          <div class="code-block-body">
            <div><span class="cm"># 安装 CLI 工具</span></div>
            <div><span class="fn">npm</span> <span class="kw">install</span> -g <span class="str">@1boss/cli</span></div>
            <div style="margin-top:8px;"><span class="cm"># 初始化项目追踪</span></div>
            <div><span class="fn">1boss</span> <span class="kw">init</span> <span class="str">"my-awesome-project"</span></div>
            <div style="margin-top:8px;"><span class="cm"># 开始任务循环</span></div>
            <div><span class="fn">1boss</span> <span class="kw">sync</span> <span class="cm"># 自动同步代码、任务与进度</span></div>
          </div>
        </div>
      </section>

      <!-- Workflow -->
      <section id="workflow" class="section-v2 fade-up stagger-5">
        <div class="section-header-v2">
          <div class="eyebrow">工作流</div>
          <h2 class="gradient-text">三步闭环，持续交付</h2>
          <p>从收集到发布的完整链路，每一步都有工具支撑</p>
        </div>
        <div class="workflow-grid-v2">
          <div class="workflow-card-v2">
            <div class="step-num">01 / 收集</div>
            <h3>收件箱</h3>
            <p>随时记录灵感，不遗漏任何想法。支持语音速记、剪贴板抓取和浏览器插件一键收藏。</p>
          </div>
          <div class="workflow-card-v2">
            <div class="step-num">02 / 规划</div>
            <h3>列表</h3>
            <p>将想法转化为可执行的任务清单。自动排期、依赖追踪、工时估算，让计划不再纸上谈兵。</p>
          </div>
          <div class="workflow-card-v2">
            <div class="step-num">03 / 交付</div>
            <h3>发布</h3>
            <p>按节奏推进，持续交付成果。Git 集成自动关联提交与任务，周报自动生成。</p>
          </div>
        </div>
      </section>

      <!-- Proof -->
      <section id="proof" class="section-v2 fade-up stagger-5">
        <div class="section-header-v2">
          <div class="eyebrow">数据反馈</div>
          <h2 class="gradient-text">独立开发者的实际效果</h2>
          <p>用数据说话，真实的效率提升</p>
        </div>
        <div class="stats-grid-v2">
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#34d399;text-shadow:0 0 30px rgba(52,211,153,0.3);">-38%</div>
            <div class="stat-label-v2">规划耗时</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#38bdf8;text-shadow:0 0 30px rgba(56,189,248,0.3);">+2.4x</div>
            <div class="stat-label-v2">任务完成量</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#a78bfa;text-shadow:0 0 30px rgba(167,139,250,0.3);">&lt;12h</div>
            <div class="stat-label-v2">想法到任务延迟</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#fbbf24;text-shadow:0 0 30px rgba(251,191,36,0.3);">91%</div>
            <div class="stat-label-v2">专注保持率</div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="section-v2 fade-up stagger-5">
        <div class="cta-section-v2">
          <h2 class="gradient-text">准备好接管你的项目了吗？</h2>
          <p>加入 2,400+ 独立开发者，用 1boss 把一人团队变成一支军团</p>
          <div class="hero-actions" style="justify-content:center;">
            <button class="btn light" style="padding:12px 28px;font-size:15px;font-weight:600;">免费开始使用</button>
            <button class="btn" style="padding:12px 28px;font-size:15px;">查看文档</button>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer style="text-align:center;padding:40px 0 20px;border-top:1px solid rgba(255,255,255,0.04);margin-top:20px;">
        <div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:16px;">
          <img src="/logo.png" alt="1boss" style="width:20px;height:20px;border-radius:5px;" />
          <span style="font-weight:700;font-size:14px;">1boss</span>
        </div>
        <p style="font-size:12px;color:var(--text-tertiary);">One App, Built for Solopreneurs.</p>
        <p style="font-size:11px;color:var(--text-tertiary);margin-top:8px;"> 2025 1boss. All rights reserved.</p>
      </footer>
    </div>
  </div>
</template>
