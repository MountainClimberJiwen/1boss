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
          <a href="#features">Features</a>
          <a href="#workflow">Workflow</a>
          <a href="#proof">Data</a>
          <a href="#integrate">Integrate</a>
        </nav>
        <div class="hero-actions">
          <RouterLink class="btn small" to="/auth">Sign In</RouterLink>
          <button class="btn light small">Get Started</button>
          <RouterLink class="btn small" to="/website/zh">ZH</RouterLink>
        </div>
      </header>

      <!-- Hero -->
      <section class="hero-main fade-up stagger-1" style="align-items:center;margin-bottom:80px;grid-template-columns:minmax(0,1fr) 480px;">
        <div>
          <div class="eyebrow" style="margin-bottom:20px;">Built for solopreneurs</div>
          <h1 class="hero-title-v2 gradient-text">one boss<br />one army</h1>
          <p class="hero-desc-v2">
            Trace project lifecycle, task loops, and idea backlogs with one technical dashboard. Focus on shipping, let a one-person team operate with the execution power of a full squad.
          </p>
          <div class="hero-actions">
            <button class="btn light" style="padding:10px 20px;font-size:14px;">Start Free</button>
            <button class="btn" style="padding:10px 20px;font-size:14px;">Book a Demo</button>
          </div>
          <div style="display:flex;align-items:center;gap:20px;margin-top:28px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              Free forever to start
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              Setup in 3 minutes
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-tertiary);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              Open-source core
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
              <span style="font-weight:700;font-size:13px;">Execution Board</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);">Live</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status running"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">Task merge</span>
              <span style="font-size:11px;color:#34d399;font-family:var(--font-mono);">running</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">10s</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status queued"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">Idea sync</span>
              <span style="font-size:11px;color:#fbbf24;font-family:var(--font-mono);">queued</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">04s</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status done"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">Doc generate</span>
              <span style="font-size:11px;color:#38bdf8;font-family:var(--font-mono);">done</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">2m</span>
            </div>
            <div class="mockup-row">
              <span class="mockup-status running"></span>
              <span style="font-size:12px;font-weight:500;flex:1;">Dependency check</span>
              <span style="font-size:11px;color:#34d399;font-family:var(--font-mono);">running</span>
              <span style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);width:40px;text-align:right;">15s</span>
            </div>
            <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.04);display:flex;gap:12px;">
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#22d3ee;">12</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">Active projects</div>
              </div>
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#a78bfa;">87%</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">Week done</div>
              </div>
              <div style="flex:1;padding:10px;background:rgba(255,255,255,0.02);border-radius:8px;text-align:center;">
                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);color:#34d399;">3</div>
                <div style="font-size:10px;color:var(--text-tertiary);margin-top:2px;">Pending ideas</div>
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
            <div class="stat-label-v2">Solopreneurs</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 purple">150K+</div>
            <div class="stat-label-v2">Tasks shipped</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 pink">12K+</div>
            <div class="stat-label-v2">Ideas captured</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2 amber">99.9%</div>
            <div class="stat-label-v2">Uptime</div>
          </div>
        </div>
      </section>

      <!-- Features -->
      <section id="features" class="section-v2 fade-up stagger-3">
        <div class="section-header-v2">
          <div class="eyebrow">Core capabilities</div>
          <h2 class="gradient-text">Full-stack control, solo</h2>
          <p>From spark to ship — every step optimized for the one-person team</p>
        </div>
        <div class="feature-grid-v2">
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(34,211,238,0.15),rgba(34,211,238,0.05));border:1px solid rgba(34,211,238,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
            <h3>Capture ideas instantly</h3>
            <p>Drop raw ideas into tasks and keep thoughts linked to execution flow. Voice memos, clipboard capture, browser extension — any way you think.</p>
          </div>
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(167,139,250,0.15),rgba(167,139,250,0.05));border:1px solid rgba(167,139,250,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
            </div>
            <h3>Decompose inbound work</h3>
            <p>Turn ideas into accepted tasks with acceptance criteria and owners. AI-assisted estimation, dependency tracking, and auto-scheduling.</p>
          </div>
          <div class="feature-card-v2">
            <div class="feature-icon" style="background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.05));border:1px solid rgba(52,211,153,0.2);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <h3>Ship in tight loops</h3>
            <p>Operate weekly sprint cycles with clear next actions and metrics. Git integration auto-links commits to tasks, weekly reports write themselves.</p>
          </div>
        </div>
      </section>

      <!-- Code Integration -->
      <section id="integrate" class="section-v2 fade-up stagger-4">
        <div class="section-header-v2">
          <div class="eyebrow">Plug & Play</div>
          <h2 class="gradient-text">One command, live in seconds</h2>
          <p>No changes to your existing stack. Integrate in 3 minutes and start tracking your first project.</p>
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
            <div><span class="cm"># Install CLI</span></div>
            <div><span class="fn">npm</span> <span class="kw">install</span> -g <span class="str">@1boss/cli</span></div>
            <div style="margin-top:8px;"><span class="cm"># Initialize project tracking</span></div>
            <div><span class="fn">1boss</span> <span class="kw">init</span> <span class="str">"my-awesome-project"</span></div>
            <div style="margin-top:8px;"><span class="cm"># Start the loop</span></div>
            <div><span class="fn">1boss</span> <span class="kw">sync</span> <span class="cm"># auto-sync code, tasks & progress</span></div>
          </div>
        </div>
      </section>

      <!-- Workflow -->
      <section id="workflow" class="section-v2 fade-up stagger-5">
        <div class="section-header-v2">
          <div class="eyebrow">Workflow</div>
          <h2 class="gradient-text">Three-step loop, ship continuously</h2>
          <p>From capture to release — every step has tooling support</p>
        </div>
        <div class="workflow-grid-v2">
          <div class="workflow-card-v2">
            <div class="step-num">01 / Capture</div>
            <h3>Inbox</h3>
            <p>Collect inspiration anytime without losing a single thought. Voice memos, clipboard grab, browser plugin one-click save.</p>
          </div>
          <div class="workflow-card-v2">
            <div class="step-num">02 / Plan</div>
            <h3>Spec</h3>
            <p>Turn ideas into actionable task lists with clear owners. Auto-scheduling, dependency tracking, effort estimation — no more planning on paper.</p>
          </div>
          <div class="workflow-card-v2">
            <div class="step-num">03 / Ship</div>
            <h3>Deliver</h3>
            <p>Push forward rhythmically and ship results continuously. Git integration auto-links commits to tasks, weekly reports generate themselves.</p>
          </div>
        </div>
      </section>

      <!-- Proof -->
      <section id="proof" class="section-v2 fade-up stagger-5">
        <div class="section-header-v2">
          <div class="eyebrow">Proof</div>
          <h2 class="gradient-text">Real gains from focused builders</h2>
          <p>Let the numbers speak — actual efficiency improvements</p>
        </div>
        <div class="stats-grid-v2">
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#34d399;text-shadow:0 0 30px rgba(52,211,153,0.3);">-38%</div>
            <div class="stat-label-v2">Planning time</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#38bdf8;text-shadow:0 0 30px rgba(56,189,248,0.3);">+2.4x</div>
            <div class="stat-label-v2">Tasks completed</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#a78bfa;text-shadow:0 0 30px rgba(167,139,250,0.3);">&lt;12h</div>
            <div class="stat-label-v2">Idea-to-task lag</div>
          </div>
          <div class="stat-item-v2">
            <div class="stat-value-v2" style="color:#fbbf24;text-shadow:0 0 30px rgba(251,191,36,0.3);">91%</div>
            <div class="stat-label-v2">Focus retention</div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="section-v2 fade-up stagger-5">
        <div class="cta-section-v2">
          <h2 class="gradient-text">Ready to take command?</h2>
          <p>Join 2,400+ solopreneurs using 1boss to turn one-person teams into armies</p>
          <div class="hero-actions" style="justify-content:center;">
            <button class="btn light" style="padding:12px 28px;font-size:15px;font-weight:600;">Get Started Free</button>
            <button class="btn" style="padding:12px 28px;font-size:15px;">View Docs</button>
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
