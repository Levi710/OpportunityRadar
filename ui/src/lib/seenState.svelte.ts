import { browser } from '$app/environment';

function createSeenState() {
  let ids = $state(new Set<number>());

  if (browser) {
    const raw = localStorage.getItem('or_seen_ids');
    if (raw) {
      try {
        ids = new Set(JSON.parse(raw));
      } catch {}
    }
  }

  return {
    get ids() { return ids; },
    markSeen: (id: number) => {
      if (!browser) return;
      ids.add(id);
      ids = new Set(ids); // Trigger reactivity
      localStorage.setItem('or_seen_ids', JSON.stringify([...ids]));
    },
    sync: () => {
      if (!browser) return;
      const raw = localStorage.getItem('or_seen_ids');
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          ids = new Set(parsed);
        } catch {}
      }
    }
  };
}

export const seenState = createSeenState();
