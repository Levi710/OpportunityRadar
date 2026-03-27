<script lang="ts">
  const sections = [
    {
      title: '🚀 Smart Feed',
      content: 'The Feed is your central hub. Our scraper checks 25+ official sources every 6 hours. When a change is detected, a new entry appears here. Look for the <span class="text-orange-primary font-bold">orange dot</span> — it indicates an update you haven\'t seen yet.'
    },
    {
      title: '🎯 Personalization',
      content: 'Don\'t get overwhelmed by irrelevant info. Go to <a href="/settings" class="text-orange-primary hover:underline font-medium">Settings</a> to set your Branch and Year. The Feed will then prioritize opportunities tagged for your profile, shown with a dedicated notification banner.'
    },
    {
      title: '📁 Categories',
      content: 'Use the sidebar to filter by type. We categorize opportunities into Certifications, Hackathons, Internships, Scholarships, and Government schemes. Each category has its own counter showing how many updates happened in the last 24 hours.'
    },
    {
      title: '🔍 Official Sources',
      content: 'We only track official platforms like NPTEL, AICTE, and Government portals. You can see the full list of monitored sites in the <a href="/sources" class="text-orange-primary hover:underline font-medium">Sources</a> tab, along with their current status and categorized tags.'
    }
  ];
</script>

<svelte:head>
  <title>Guide — OpportunityRadar</title>
</svelte:head>

<div class="max-w-3xl">
  <header class="mb-14">
    <h1 class="text-3xl font-bold text-silver-primary italic tracking-tight">How to use OpportunityRadar</h1>
    <p class="text-silver-muted mt-4 text-lg/relaxed">A quick guide for students to stay ahead of the curve.</p>
  </header>

  <div class="space-y-16">
    {#each sections as section}
      <section class="border-l-2 border-orange-primary/20 pl-10 relative pb-2">
        <div class="absolute -left-[6px] top-1.5 w-2.5 h-2.5 rounded-full bg-orange-primary shadow-[0_0_12px_rgba(255,107,0,0.6)]"></div>
        <h2 class="text-xl font-semibold text-silver-primary mb-4 flex items-center gap-3">
          {section.title}
        </h2>
        <div class="text-silver-muted leading-7 text-[15.5px]">
          {@html section.content}
        </div>
      </section>
    {/each}
  </div>

  <div class="mt-20 bg-bg-secondary border border-border rounded-2xl p-10 flex flex-col items-center text-center gap-8">
    <div class="space-y-3">
      <h3 class="text-xl font-bold text-silver-primary">Ready to start?</h3>
      <p class="text-silver-muted max-w-md">Set your profile now to see the most relevant opportunities tailored for your branch.</p>
    </div>
    <a 
      href="/settings" 
      class="inline-flex items-center justify-center bg-orange-primary text-[#0F0F0F] px-10 py-3.5 rounded-lg font-bold no-underline hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg shadow-orange-primary/10"
    >
      Configure Settings
    </a>
  </div>

  <footer class="mt-24 py-12 border-t border-border flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-silver-subtle uppercase tracking-widest">
    <p>© 2026 OpportunityRadar V3</p>
    <div class="flex items-center gap-6">
      <p>Last update: March 2026</p>
      <p>Version: 3.0.1</p>
    </div>
  </footer>
</div>
