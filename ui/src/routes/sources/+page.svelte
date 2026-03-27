<script lang="ts">
  import { timeAgo, truncate, isWithin24h } from '$lib/utils';

  let { data } = $props();
</script>

<svelte:head>
  <title>Sources — OpportunityRadar</title>
</svelte:head>

<div>
  <!-- Header -->
  <div class="mb-10">
    <h1 class="text-2xl font-medium text-silver-primary">Sources</h1>
    <p class="text-[13px] text-silver-muted mt-2">All monitored official sources</p>
  </div>

  <!-- Table -->
  <div class="overflow-x-auto">
    <table class="w-full text-left">
      <thead>
        <tr class="text-xs uppercase tracking-[0.08em] text-silver-subtle">
          <th class="pb-3 pr-4 font-medium">Name</th>
          <th class="pb-3 pr-4 font-medium hidden sm:table-cell">URL</th>
          <th class="pb-3 pr-4 font-medium">Type</th>
          <th class="pb-3 pr-4 font-medium">Status</th>
          <th class="pb-3 pr-4 font-medium hidden md:table-cell">Last checked</th>
          <th class="pb-3 font-medium hidden md:table-cell">Last changed</th>
        </tr>
      </thead>
      <tbody>
        {#each data.sources as source}
          <tr class="border-b border-border transition-colors duration-150 hover:bg-bg-tertiary">
            <td class="py-3 pr-4 text-sm text-silver-primary">{source.name}</td>
            <td class="py-3 pr-4 text-xs text-silver-subtle hidden sm:table-cell">
              <a href={source.url} target="_blank" rel="noopener noreferrer" class="text-silver-subtle hover:text-orange-primary no-underline">
                {truncate(source.url, 40)}
              </a>
            </td>
            <td class="py-3 pr-4">
              {#if source.is_js_rendered}
                <span class="text-[11px] bg-orange-subtle text-orange-muted px-2 py-0.5 rounded">JS</span>
              {:else}
                <span class="text-[11px] bg-bg-tertiary text-silver-muted px-2 py-0.5 rounded">Static</span>
              {/if}
            </td>
            <td class="py-3 pr-4">
              {#if source.active}
                <span class="text-[11px] bg-[#0A1A0A] text-[#4A9A4A] px-2 py-0.5 rounded">Active</span>
              {:else}
                <span class="text-[11px] bg-bg-tertiary text-silver-subtle px-2 py-0.5 rounded">Paused</span>
              {/if}
            </td>
            <td class="py-3 pr-4 text-xs text-silver-subtle hidden md:table-cell">
              {source.last_checked ? timeAgo(source.last_checked) : '—'}
            </td>
            <td class="py-3 text-xs hidden md:table-cell
              {source.last_changed && isWithin24h(source.last_changed) ? 'text-orange-primary' : 'text-silver-subtle'}">
              {source.last_changed ? timeAgo(source.last_changed) : '—'}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  {#if data.sources.length === 0}
    <div class="text-center py-20">
      <p class="text-silver-subtle text-sm">No sources configured yet.</p>
    </div>
  {/if}
</div>
