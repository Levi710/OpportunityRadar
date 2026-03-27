import type { PageServerLoad } from './$types';
import { getChanges } from '$lib/db';

export const load: PageServerLoad = async ({ parent }) => {
  const { profile } = await parent();
  const branch = profile?.branch;

  const changes = getChanges({
    category: 'scholarships',
    branch: branch === 'all' ? undefined : branch,
    limit: 50
  });

  return {
    changes,
    categoryName: 'Scholarships',
    categoryDesc: 'Financial aid and fellowships'
  };
};
