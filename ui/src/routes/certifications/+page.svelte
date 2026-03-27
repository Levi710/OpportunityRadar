<script lang="ts">
  import FeedList from '$lib/components/FeedList.svelte';

  let { data } = $props();
</script>

<svelte:head>
  <title>{data.categoryName} — OpportunityRadar</title>
</svelte:head>

<div>
  <header class="mb-10">
    <h1 class="text-2xl font-medium text-silver-primary">{data.categoryName}</h1>
    <p class="text-[13px] text-silver-muted mt-2">{data.categoryDesc}</p>
  </header>

  <FeedList changes={data.changes} emptyMessage="No {data.categoryName.toLowerCase()} detected recently." />
</div>
