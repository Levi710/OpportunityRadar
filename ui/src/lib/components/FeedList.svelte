<script lang="ts">
  import { timeAgo, extractDomain } from '$lib/utils';
  import type { ChangeEvent } from '$lib/types';
  import { seenState } from '$lib/seenState.svelte';

  let { changes, emptyMessage = "No changes detected yet." } = $props();

  function isNew(id: number): boolean {
    return !seenState.ids.has(id);
  }

  const categoryStyles: Record<string, string> = {
    certifications: 'bg-[#0A1A1A] text-[#4A9A8A]',
    hackathons: 'bg-[#1A0E08] text-[#F97316]',
    internships: 'bg-[#0A0A1A] text-[#6A7ACA]',
    scholarships: 'bg-[#1A1A0A] text-[#9A9A4A]',
    government: 'bg-[#0A1A0A] text-[#4A9A4A]'
  };
</script>

{#if changes.length === 0}
  <div class="text-center py-20">
    <p class="text-silver-subtle text-sm">{emptyMessage}</p>
    <p class="text-silver-subtle text-sm mt-1">The system checks every 6 hours.</p>
  </div>
{:else}
  <div class="flex flex-col gap-px overflow-hidden rounded-[6px] border border-border">
    {#each changes as change}
      <div
        class="bg-bg-secondary p-5 transition-colors duration-150 hover:bg-bg-tertiary border-b border-border last:border-b-0"
        onmouseenter={() => seenState.markSeen(change.id)}
      >
        <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
          <div class="flex flex-wrap items-center gap-2.5">
            {#if isNew(change.id)}
              <span class="w-1.5 h-1.5 rounded-full bg-orange-primary flex-shrink-0"></span>
            {/if}
            <span class="text-[13px] font-medium text-silver-primary">{change.source_name}</span>
            <span class="text-[11px] uppercase tracking-[0.1em] px-2.5 py-1 rounded-[5px] font-bold {categoryStyles[change.category] || 'bg-bg-tertiary text-silver-muted'}">
              {change.category}
            </span>
          </div>
          <span class="text-xs text-silver-subtle flex-shrink-0">{timeAgo(change.checked_at)}</span>
        </div>

        <p class="text-sm text-silver-muted mt-2 ml-4">
          New content detected on {change.source_name.toLowerCase()} page
        </p>

        <div class="flex items-center justify-between mt-3 ml-4">
          <span class="text-xs text-silver-subtle">{extractDomain(change.source_url)}</span>
          <a
            href={change.source_url}
            target="_blank"
            rel="noopener noreferrer"
            onclick={() => seenState.markSeen(change.id)}
            class="text-[13px] text-orange-primary hover:text-white transition-colors duration-150 no-underline"
          >
            View →
          </a>
        </div>
      </div>
    {/each}
  </div>
{/if}
