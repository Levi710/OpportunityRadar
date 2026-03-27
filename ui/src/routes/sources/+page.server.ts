import type { PageServerLoad } from './$types';
import { getAllSources } from '$lib/db';

export const load: PageServerLoad = () => {
  const sources = getAllSources();

  return {
    sources
  };
};
