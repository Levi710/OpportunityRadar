import type { PageServerLoad } from './$types';
import { getChanges } from '$lib/db';

export const load: PageServerLoad = async ({ parent }) => {
  const { profile } = await parent();
  const branch = profile?.branch;

  const changes = getChanges({
    category: 'hackathons',
    branch: branch === 'all' ? undefined : branch,
    limit: 50
  });

  return {
    changes,
    categoryName: 'Hackathons',
    categoryDesc: 'Competitive events and coding challenges'
  };
};
