import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { upsertStudentProfile } from '$lib/db';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const profile = await request.json();
    
    // Simple validation
    if (!profile.branch || !profile.year) {
      return json({ success: false, error: 'Branch and Year are required' }, { status: 400 });
    }

    upsertStudentProfile({
      name: profile.name || '',
      college: profile.college || '',
      branch: profile.branch,
      year: parseInt(profile.year),
    });

    return json({ success: true });
  } catch (err: any) {
    return json({ success: false, error: err.message }, { status: 500 });
  }
};
