import type { PageServerLoad } from './$types';
import { getChanges } from '$lib/db';

export const load: PageServerLoad = async ({ url, parent }) => {
  const { profile } = await parent();
  const filter = url.searchParams.get('filter') || 'all';
  const branch = profile?.branch;

  let sinceUtc: string | undefined;
  if (filter === 'today') {
    sinceUtc = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  } else if (filter === 'week') {
    const lastWeek = new Date();
    lastWeek.setDate(lastWeek.getDate() - 7);
    sinceUtc = lastWeek.toISOString().split('T')[0];
  }

  const changes = getChanges({
    branch: branch === 'all' ? undefined : branch,
    sinceUtc,
    limit: 50
  });

  const { getLastCheckedTime } = await import('$lib/db');
  const lastCheckedTime = getLastCheckedTime();

  return {
    changes,
    filter,
    lastCheckedTime
  };
};
