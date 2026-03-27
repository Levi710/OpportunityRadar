import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { upsertStudentProfile } from '$lib/db';

export const POST: RequestHandler = async ({ request, cookies }) => {
  try {
    const profileData = await request.json();
    
    // Simple validation
    if (!profileData.branch || !profileData.year) {
      return json({ success: false, error: 'Branch and Year are required' }, { status: 400 });
    }

    const currentCookie = cookies.get('student_profile');
    let updateCount = 0;
    
    if (currentCookie) {
      try {
        const existing = JSON.parse(currentCookie);
        updateCount = (existing.update_count || 0);

        // Limit check
        if (updateCount >= 2) {
          return json({ success: false, error: 'Maximum updates reached for this browser (2/2)' }, { status: 403 });
        }
        updateCount++;
      } catch (e) { /* corrupted cookie - reset count */ }
    }

    const newProfile = {
      name: profileData.name || '',
      college: profileData.college || '',
      branch: profileData.branch,
      year: parseInt(profileData.year),
      update_count: updateCount
    };

    cookies.set('student_profile', JSON.stringify(newProfile), {
      path: '/',
      maxAge: 60 * 60 * 24 * 365, // 1 year
      httpOnly: false, // Let client JS read if needed
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production'
    });

    return json({ success: true });
  } catch (err: any) {
    return json({ success: false, error: err.message }, { status: 500 });
  }
};
