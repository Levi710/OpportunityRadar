<script lang="ts">
  import { invalidateAll } from '$app/navigation';

  let { data } = $props();

  let name = $state(data.profile?.name || '');
  let college = $state(data.profile?.college || '');
  let branch = $state(data.profile?.branch || 'cs');
  let year = $state(data.profile?.year || 1);
  let saving = $state(false);
  let message = $state('');

  const branches = [
    { slug: 'all', label: 'All Branches' },
    { slug: 'cs', label: 'Computer Science' },
    { slug: 'it', label: 'Information Technology' },
    { slug: 'ece', label: 'Electronics & Communication' },
    { slug: 'eee', label: 'Electrical & Electronics' },
    { slug: 'mech', label: 'Mechanical Engineering' },
    { slug: 'civil', label: 'Civil Engineering' },
    { slug: 'chem', label: 'Chemical Engineering' },
    { slug: 'bio', label: 'Biotechnology' },
    { slug: 'management', label: 'Management' },
    { slug: 'other', label: 'Other' }
  ];

  async function saveProfile() {
    saving = true;
    message = '';
    
    try {
      const res = await fetch('/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, college, branch, year })
      });
      
      const result = await res.json();
      if (result.success) {
        message = 'Profile saved.';
        await invalidateAll();
      } else {
        message = 'Error: ' + result.error;
      }
    } catch (err: any) {
      message = 'Error saving profile.';
    } finally {
      saving = false;
    }
  }
</script>

<div class="max-w-2xl">
  <header class="mb-10">
    <h1 class="text-3xl font-bold text-silver-primary">Your profile</h1>
    <p class="text-silver-subtle mt-2">Set your branch and year to filter what's relevant to you.</p>
  </header>

  <div class="border-t border-border mb-8"></div>

  <div class="space-y-8">
    <div class="grid grid-cols-1 sm:grid-cols-[120px_1fr] items-center gap-4">
      <label for="name" class="text-sm text-silver-muted">Name</label>
      <input
        id="name"
        type="text"
        bind:value={name}
        placeholder="Enter your name"
        class="bg-[#1E1E1E] border border-[#2A2A2A] text-silver-primary p-[10px_14px] rounded-md outline-none focus:border-orange-primary transition-colors"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-[120px_1fr] items-center gap-4">
      <label for="college" class="text-sm text-silver-muted">College</label>
      <input
        id="college"
        type="text"
        bind:value={college}
        placeholder="Enter your college"
        class="bg-[#1E1E1E] border border-[#2A2A2A] text-silver-primary p-[10px_14px] rounded-md outline-none focus:border-orange-primary transition-colors"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-[120px_1fr] items-center gap-4">
      <label for="branch" class="text-sm text-silver-muted">Branch</label>
      <select
        id="branch"
        bind:value={branch}
        class="bg-[#1E1E1E] border border-[#2A2A2A] text-silver-primary p-[10px_14px] rounded-md outline-none focus:border-orange-primary transition-colors appearance-none"
      >
        {#each branches as b}
          <option value={b.slug} class="bg-[#1E1E1E]">{b.label}</option>
        {/each}
      </select>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-[120px_1fr] items-center gap-4">
      <span class="text-sm text-silver-muted">Year</span>
      <div class="flex gap-2">
        {#each [1, 2, 3, 4] as y}
          <button
            onclick={() => year = y}
            class="w-10 h-10 rounded-md transition-colors duration-150 border border-transparent
              {year === y ? 'bg-orange-primary text-[#0F0F0F] font-bold' : 'bg-[#1E1E1E] text-silver-muted border-[#2A2A2A] hover:border-silver-subtle'}"
          >
            {y}
          </button>
        {/each}
      </div>
    </div>

    <div class="flex flex-col items-start gap-4 pt-4 sm:ml-[120px]">
      <button
        onclick={saveProfile}
        disabled={saving}
        class="bg-orange-primary text-[#0F0F0F] text-sm font-semibold px-8 py-2.5 rounded-md hover:bg-orange-primary/90 transition-opacity disabled:opacity-50"
      >
        {saving ? 'Saving...' : 'Save profile'}
      </button>
      
      {#if message}
        <p class="text-sm text-silver-subtle italic">{message}</p>
      {/if}
    </div>
  </div>
</div>
