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
          <a href="#features">Features</a>
          <a href="#workflow">Workflow</a>
          <a href="#proof">Proof</a>
        </nav>
        <div class="hero-actions">
          <RouterLink class="btn small" to="/auth">Sign In</RouterLink>
          <button class="btn light small">Get Started</button>
          <RouterLink class="btn small" to="/website/zh">ZH</RouterLink>
        </div>
      </header>

      <!-- Hero -->
      <section class="hero-main" style="align-items:center;margin-bottom:32px;">
        <div class="fade-up stagger-1">
          <div class="eyebrow">Built for solopreneurs</div>
          <h1 class="title" style="font-size:52px;max-width:12ch;">one boss<br />one army</h1>
          <p class="section-sub" style="font-size:14px;max-width:48ch;margin-top:16px;">
            Trace project lifecycle, task loops, and idea backlogs with one technical dashboard for focused solopreneurs.
          </p>
          <div class="hero-actions" style="margin-top:24px;">
            <button class="btn light">Start Free</button>
            <button class="btn">Book a 15m Walkthrough</button>
          </div>
        </div>
        <div class="hero-panel fade-up stagger-2" style="position:relative;">
          <div style="position:absolute;top:-40px;right:-20px;width:120px;height:120px;border-radius:999px;background:radial-gradient(circle,rgba(59,130,246,0.12),transparent 70%);filter:blur(40px);pointer-events:none;"></div>
          <div style="font-weight:700;margin-bottom:12px;font-size:14px;">Live Execution Board</div>
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Task</th>
                  <th>Status</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="font-weight:500;">task merge</td>
                  <td>
                    <span style="display:inline-flex;align-items:center;gap:6px;">
                      <span class="unread-badge" style="width:6px;height:6px;margin:0;animation:none;background:#34d399;box-shadow:0 0 6px rgba(52,211,153,0.4);"></span>
                      running
                    </span>
                  </td>
                  <td class="mono">10s</td>
                </tr>
                <tr>
                  <td style="font-weight:500;">idea sync</td>
                  <td>
                    <span style="display:inline-flex;align-items:center;gap:6px;">
                      <span class="unread-badge" style="width:6px;height:6px;margin:0;animation:none;background:#fbbf24;box-shadow:0 0 6px rgba(251,191,36,0.4);"></span>
                      queued
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
            <div class="eyebrow" style="margin-bottom:10px;">Core capabilities</div>
            <div style="font-weight:700;font-size:16px;">For technical solo operators</div>
          </div>
        </div>
        <div class="grid-3">
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(56,189,248,0.15),rgba(56,189,248,0.05));border:1px solid rgba(56,189,248,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">Capture ideas instantly</div>
            <p class="section-sub" style="margin:0;">Drop raw ideas into tasks and keep thoughts linked to execution flow.</p>
          </div>
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(167,139,250,0.15),rgba(167,139,250,0.05));border:1px solid rgba(167,139,250,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">Decompose inbound work</div>
            <p class="section-sub" style="margin:0;">Turn ideas into accepted tasks with acceptance criteria and owners.</p>
          </div>
          <div class="card" style="background:var(--panel-2);">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,rgba(52,211,153,0.15),rgba(52,211,153,0.05));border:1px solid rgba(52,211,153,0.15);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:16px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
            <div class="kpi-label" style="margin-top:0;margin-bottom:6px;">Ship in tight loops</div>
            <p class="section-sub" style="margin:0;">Operate weekly sprint cycles with clear next actions and metrics.</p>
          </div>
        </div>
      </section>

      <!-- Workflow -->
      <section id="workflow" class="hero-panel fade-up stagger-4" style="margin-bottom:14px;">
        <div class="eyebrow" style="margin-bottom:10px;">Workflow</div>
        <div style="font-weight:700;font-size:16px;margin-bottom:16px;">How 1boss works in practice</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">01. Capture</div>
            <div class="section-title" style="font-size:22px;margin:0;">Inbox</div>
            <p class="section-sub" style="margin:8px 0 0;">Collect inspiration anytime without losing a single thought.</p>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">02. Plan</div>
            <div class="section-title" style="font-size:22px;margin:0;">Spec</div>
            <p class="section-sub" style="margin:8px 0 0;">Turn ideas into actionable task lists with clear owners.</p>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">03. Ship</div>
            <div class="section-title" style="font-size:22px;margin:0;">Deliver</div>
            <p class="section-sub" style="margin:8px 0 0;">Push forward rhythmically and ship results continuously.</p>
          </div>
        </div>
      </section>

      <!-- Proof -->
      <section id="proof" class="hero-panel fade-up stagger-5">
        <div class="eyebrow" style="margin-bottom:10px;">Proof</div>
        <div style="font-weight:700;font-size:16px;margin-bottom:16px;">From focused builders</div>
        <div class="grid-4">
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">Planning time</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#34d399;">-38%</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">Tasks completed</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#38bdf8;">+2.4x</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">Idea-to-task lag</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#a78bfa;">&lt;12h</div>
          </div>
          <div style="padding:16px;background:var(--panel-2);border-radius:12px;border:1px solid var(--line);text-align:center;transition:all var(--duration-slow) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
            <div class="kpi-label" style="margin-top:0;margin-bottom:8px;">Focus retention</div>
            <div class="section-title" style="font-size:28px;margin:0;color:#fbbf24;">91%</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
