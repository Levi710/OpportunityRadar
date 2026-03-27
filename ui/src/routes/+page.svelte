<script lang="ts">
  import FeedList from '$lib/components/FeedList.svelte';

  let { data } = $props();

  const filters = [
    { label: 'All', value: 'all' },
    { label: 'Today', value: 'today' },
    { label: 'This week', value: 'week' }
  ];

  const branchLabels: Record<string, string> = {
    cs: 'Computer Science',
    it: 'Information Technology',
    ece: 'Electronics & Communication',
    eee: 'Electrical & Electronics',
    mech: 'Mechanical Engineering',
    civil: 'Civil Engineering',
    chem: 'Chemical Engineering',
    bio: 'Biotechnology',
    management: 'Management',
    other: 'Other',
    all: 'All Branches'
  };
</script>

<svelte:head>
  <title>Feed — OpportunityRadar</title>
</svelte:head>

<div>
  <!-- Header -->
  <div class="mb-8">
    <h1 class="text-2xl font-medium text-silver-primary">All updates</h1>
    <p class="text-[13px] text-silver-muted mt-2">Showing changes from all monitored sources</p>
  </div>

  <!-- Profile Banner -->
  {#if data.profile}
    <div class="mb-8 bg-[#1A0E08] border border-[#2A2A2A] rounded-md p-[12px_20px] flex items-center justify-between">
      <div class="text-sm text-silver-muted">
        Showing results relevant to <span class="text-orange-primary font-medium">{branchLabels[data.profile.branch] || data.profile.branch}</span> · Year {data.profile.year}
      </div>
      <a href="/settings" class="text-[12px] text-orange-primary hover:underline font-medium">Edit</a>
    </div>
  {:else}
    <div class="mb-8 bg-bg-secondary border border-border rounded-md p-3 text-center">
      <p class="text-sm text-silver-subtle">
        <a href="/settings" class="text-orange-primary hover:underline">Set your branch in Settings</a> to see personalised results.
      </p>
    </div>
  {/if}

  <!-- Filter bar -->
  <div class="flex flex-wrap gap-3 mb-10">
    {#each filters as f}
      <a
        href="/?filter={f.value}"
        class="inline-flex items-center justify-center px-4 py-1.5 text-sm font-medium rounded-sm no-underline transition-colors duration-150 min-w-[70px]
          {data.filter === f.value
            ? 'bg-orange-primary text-white!'
            : 'bg-bg-tertiary text-silver-muted! border border-border hover:text-silver-primary!'}"
      >
        {f.label}
      </a>
    {/each}
  </div>

  <FeedList changes={data.changes} />
</div>
