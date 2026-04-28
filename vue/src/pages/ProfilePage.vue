<template>
  <DashboardLayout active="reports">
    <div class="topbar">
      <div>
        <div style="font-size:28px;font-weight:700;">个人主页</div>
        <div class="subtitle">管理你的账号信息、工作偏好与会话状态。</div>
      </div>
      <button class="btn">返回 Task List</button>
    </div>

    <div class="profile-layout">
      <div class="card">
        <div style="font-weight:600;margin-bottom:10px;">个人资料</div>
        <div class="subtitle" style="margin-bottom:4px;">姓名</div><input class="input" value="John Doe" />
        <div class="subtitle" style="margin:10px 0 4px;">邮箱</div><input class="input" value="john@company.com" />
        <div class="subtitle" style="margin:10px 0 4px;">手机号</div><input class="input" value="+86 138 0000 0000" />
        <button class="btn light" style="margin-top:12px;">保存修改</button>
      </div>
      <div class="side-stack">
        <div class="card"><div style="font-weight:600;margin-bottom:10px;">账号安全</div><button class="btn" style="width:100%;">管理双重验证</button></div>
        <div class="card"><div style="font-weight:600;margin-bottom:10px;">快捷操作</div><button class="btn" style="width:100%;margin-bottom:8px;">Sign out</button><button class="btn" style="width:100%;">Sign in / Register</button></div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '../layouts/DashboardLayout.vue'
</script>
