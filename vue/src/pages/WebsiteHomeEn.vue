<template>
  <div class="page-shell">
    <div class="hero-wrap">
      <header class="hero-header">
        <div class="hero-logo">
          <img class="hero-logo-img" src="/logo.png" alt="1boss logo" />
          <span>1boss</span>
        </div>
        <nav class="hero-nav"><a>Feature</a><a>Roadmap</a><a>Pricing</a></nav>
        <div class="hero-actions"><button class="btn small">Sign In</button><button class="btn light small">Get Started</button><RouterLink class="btn small" to="/website/zh">ZH</RouterLink></div>
      </header>

      <section class="hero-main">
        <div>
          <h1 class="title">one boss, one army</h1>
          <p class="section-sub">Trace project lifecycle, task loops, and idea backlogs with one technical dashboard for focused solopreneurs.</p>
          <div class="hero-actions"><button class="btn light">Start Free</button><button class="btn">Book a 15m Walkthrough</button></div>
        </div>
        <div class="hero-panel">
          <div style="font-weight:600;margin-bottom:8px;">Live Execution Board</div>
          <table class="table"><thead><tr><th>T2</th><th>42</th><th>18</th></tr></thead><tbody><tr><td>task merge</td><td>running</td><td>10s</td></tr><tr><td>idea sync</td><td>queued</td><td>04s</td></tr></tbody></table>
        </div>
      </section>

      <section class="hero-panel" style="margin-bottom:12px;"><div style="display:flex;justify-content:space-between;"><div style="font-weight:600;">Core capabilities for technical solo operators</div><button class="btn small">Get the feature overview</button></div><div class="grid-3" style="margin-top:12px;"><div class="card"><div class="kpi-label">Capture ideas instantly</div><p class="section-sub">Drop raw ideas into tasks and keep thoughts linked to execution flow.</p><button class="btn small">Collect</button></div><div class="card"><div class="kpi-label">Decompose inbound work</div><p class="section-sub">Turn ideas into accepted tasks with acceptance criteria and owners.</p><button class="btn small">Break down</button></div><div class="card"><div class="kpi-label">Ship in tight loops</div><p class="section-sub">Operate weekly sprint cycles with clear next actions and metrics.</p><button class="btn small">Execute</button></div></div></section>

      <section class="hero-panel" style="margin-bottom:12px;"><div style="font-weight:600;margin-bottom:10px;">How 1boss works in practice</div><div class="grid-3"><div class="card"><div class="kpi-label">01. Capture</div><div class="section-title" style="font-size:20px;">Inbox</div></div><div class="card"><div class="kpi-label">02. Plan</div><div class="section-title" style="font-size:20px;">Spec</div></div><div class="card"><div class="kpi-label">03. Ship</div><div class="section-title" style="font-size:20px;">Deliver</div></div></div></section>

      <section class="hero-panel"><div style="font-weight:600;margin-bottom:10px;">Proof from focused builders</div><div class="grid-4"><div class="card"><div class="kpi-label">Planning time</div><div class="section-title" style="font-size:24px;">-38%</div></div><div class="card"><div class="kpi-label">Tasks completed</div><div class="section-title" style="font-size:24px;">+2.4x</div></div><div class="card"><div class="kpi-label">Idea-to-task lag</div><div class="section-title" style="font-size:24px;">&lt;12h</div></div><div class="card"><div class="kpi-label">Focus retention</div><div class="section-title" style="font-size:24px;">91%</div></div></div></section>
    </div>
  </div>
</template>
