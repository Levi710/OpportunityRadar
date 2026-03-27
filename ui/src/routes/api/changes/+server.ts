import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getChanges } from '$lib/db';

export const GET: RequestHandler = ({ url }) => {
  const limitParam = url.searchParams.get('limit');
  const limit = limitParam ? parseInt(limitParam, 10) : 50;

  const changes = getChanges({ limit });

  return json(changes);
};
