import type { PageServerLoad } from './$types';
import { getChanges } from '$lib/db';

export const load: PageServerLoad = async ({ parent }) => {
  const { profile } = await parent();
  const branch = profile?.branch;

  const changes = getChanges({
    category: 'certifications',
    branch: branch === 'all' ? undefined : branch,
    limit: 50
  });

  return {
    changes,
    categoryName: 'Certifications',
    categoryDesc: 'Professional certificates and online courses'
  };
};
