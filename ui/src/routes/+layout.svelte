<script lang="ts">
  import '../app.css';
  import { page } from '$app/state';
  import { seenState } from '$lib/seenState.svelte';

  let { children, data } = $props();

  const mainNav = [
    { label: 'Feed', href: '/' }
  ];

  const categories = [
    { label: 'Certifications', href: '/certifications', id: 'certifications' },
    { label: 'Hackathons', href: '/hackathons', id: 'hackathons' },
    { label: 'Internships', href: '/internships', id: 'internships' },
    { label: 'Scholarships', href: '/scholarships', id: 'scholarships' },
    { label: 'Government', href: '/government', id: 'government' }
  ];

  const footerNav = [
    { label: 'Sources', href: '/sources' },
    { label: 'Settings', href: '/settings' },
    { label: 'Guide', href: '/guide' }
  ];

  let mobileMenuOpen = $state(false);

  // --- Reactive Seen State ---
  $effect(() => {
    // Sync when coming back to the tab
    window.addEventListener('focus', seenState.sync);
    return () => window.removeEventListener('focus', seenState.sync);
  });

  const unseenTodayCount = $derived(
    data.todayTotalIds.filter((id: number) => !seenState.ids.has(id)).length
  );

  const categoryUnseenCounts = $derived.by(() => {
    const counts: Record<string, number> = {};
    data.todayChangeIds.forEach((item: { id: number, category: string }) => {
      if (!seenState.ids.has(item.id)) {
        counts[item.category] = (counts[item.category] || 0) + 1;
      }
    });
    return counts;
  });
</script>

<div class="flex flex-col md:flex-row min-h-screen bg-bg-primary">
  <!-- Sidebar (desktop) -->
  <aside class="hidden md:flex flex-col w-[240px] border-r border-border bg-bg-secondary flex-shrink-0">
    <div class="p-5">
      <a href="/" class="flex items-center gap-2 no-underline">
        <span class="w-2.5 h-2.5 rounded-full bg-orange-primary flex-shrink-0"></span>
        <span class="text-[15px] font-medium text-silver-primary">OpportunityRadar</span>
      </a>
    </div>

    <div class="border-t border-border mx-4 mb-2"></div>

    <nav class="flex-1 overflow-y-auto">
      {#each mainNav as item}
        <a
          href={item.href}
          class="flex items-center justify-between pl-5 pr-3 py-2 text-sm no-underline transition-colors duration-150
            {page.url.pathname === item.href
              ? 'text-silver-primary bg-orange-subtle border-l-2 border-orange-primary'
              : 'text-silver-muted hover:bg-bg-tertiary border-l-2 border-transparent'}"
        >
          <span>{item.label}</span>
          {#if item.href === '/' && unseenTodayCount > 0}
            <span class="text-[12px] font-bold bg-orange-muted text-orange-primary px-2.5 py-1 rounded-full min-w-[24px] text-center inline-block leading-none mr-1">{unseenTodayCount}</span>
          {/if}
        </a>
      {/each}

      <div class="mt-4 mb-2 px-5 text-[10px] uppercase tracking-widest text-silver-subtle font-semibold">Categories</div>
      
      {#each categories as item}
        <a
          href={item.href}
          class="flex items-center justify-between pl-5 pr-3 py-2 text-sm no-underline transition-colors duration-150
            {page.url.pathname === item.href
              ? 'text-silver-primary bg-orange-subtle border-l-2 border-orange-primary'
              : 'text-silver-muted hover:bg-bg-tertiary border-l-2 border-transparent'}"
        >
          <span class="truncate pr-2">{item.label}</span>
          {#if (categoryUnseenCounts[item.id] || 0) > 0}
            <span class="text-[12px] font-bold bg-orange-muted text-orange-primary px-2.5 py-1 rounded-full min-w-[24px] text-center inline-block leading-none mr-1">{categoryUnseenCounts[item.id]}</span>
          {/if}
        </a>
      {/each}

      <div class="mt-4 border-t border-border mx-4 mb-2"></div>

      {#each footerNav as item}
        <a
          href={item.href}
          class="flex items-center justify-between pl-5 pr-3 py-2 text-sm no-underline transition-colors duration-150
            {page.url.pathname === item.href
              ? 'text-silver-primary bg-orange-subtle border-l-2 border-orange-primary'
              : 'text-silver-muted hover:bg-bg-tertiary border-l-2 border-transparent'}"
        >
          <span>{item.label}</span>
        </a>
      {/each}
    </nav>

    <div class="p-5 border-t border-border mt-auto">
      <p class="text-xs text-silver-subtle">Last checked</p>
      {#if data.lastChecked}
        <p class="text-xs text-silver-muted">{timeAgoDisplay(data.lastChecked)}</p>
      {:else}
        <p class="text-xs text-silver-subtle">Not yet</p>
      {/if}
    </div>
  </aside>

  <!-- Mobile top bar -->
  <div class="md:hidden sticky top-0 left-0 right-0 z-50 bg-bg-secondary border-b border-border h-14">
    <div class="flex items-center justify-between px-4 h-full">
      <a href="/" class="flex items-center gap-2 no-underline">
        <span class="w-2 h-2 rounded-full bg-orange-primary"></span>
        <span class="text-sm font-medium text-silver-primary">OpportunityRadar</span>
      </a>
      <button
        onclick={() => mobileMenuOpen = !mobileMenuOpen}
        class="text-silver-muted text-sm bg-transparent border-none cursor-pointer p-2"
        aria-label="Toggle menu"
      >
        {mobileMenuOpen ? '✕' : '☰'}
      </button>
    </div>

    {#if mobileMenuOpen}
      <nav class="absolute top-14 left-0 right-0 bg-bg-secondary border-b border-border shadow-2xl max-h-[80vh] overflow-y-auto z-50">
        {#each [...mainNav, ...footerNav] as item}
          <a
            href={item.href}
            onclick={() => mobileMenuOpen = false}
            class="flex items-center justify-between px-6 py-4 text-sm no-underline border-b border-border/50
              {page.url.pathname === item.href
                ? 'text-silver-primary bg-orange-subtle'
                : 'text-silver-muted'}"
          >
            <span>{item.label}</span>
          </a>
        {/each}
        <div class="px-6 py-2 bg-bg-primary text-[10px] uppercase tracking-widest text-silver-subtle font-semibold">Categories</div>
        {#each categories as item}
          <a
            href={item.href}
            onclick={() => mobileMenuOpen = false}
            class="flex items-center justify-between px-6 py-4 text-sm no-underline border-b border-border/50
              {page.url.pathname === item.href
                ? 'text-silver-primary bg-orange-subtle'
                : 'text-silver-muted'}"
          >
            <span>{item.label}</span>
            {#if (categoryUnseenCounts[item.id] || 0) > 0}
              <span class="text-[12px] font-bold bg-orange-muted text-orange-primary px-2.5 py-1 rounded-full min-w-[24px] text-center inline-block leading-none">{categoryUnseenCounts[item.id]}</span>
            {/if}
          </a>
        {/each}
      </nav>
    {/if}
  </div>

  <!-- Main content -->
  <main class="flex-1 md:px-10 px-5 pt-10 pb-10">
    {@render children()}
  </main>
</div>

<script lang="ts" module>
  import { timeAgo } from '$lib/utils';

  function timeAgoDisplay(dateString: string | null): string {
    if (!dateString) return 'Not yet';
    return timeAgo(dateString);
  }
</script>
