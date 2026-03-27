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

    const currentProfile = await import('$lib/db').then(db => db.getStudentProfile());
    
    // Limit to 2 saves total (initial + one update)
    // First save: currentProfile is null -> OK (Result = 0)
    // Second save: update_count=0 -> OK (Result = 1)
    // Third save: update_count=1 -> Blocked
    if (currentProfile && currentProfile.update_count >= 1) {
      return json({ success: false, error: 'Profile modification limit reached (2/2)' }, { status: 403 });
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
