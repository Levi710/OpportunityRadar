import { getSourceStats, getLastCheckedTime, getCategoryCounts, getStudentProfile, getTodayChangeIds, getTodayTotalIds } from '$lib/db';
import type { LayoutServerLoad } from './$types';

export const prerender = false;

export const load: LayoutServerLoad = ({ cookies }) => {
  const profileCookie = cookies.get('student_profile');
  let profile = null;
  if (profileCookie) {
    try {
      profile = JSON.parse(profileCookie);
    } catch (e) { /* ignore */ }
  }

  const stats = getSourceStats();
  const lastChecked = getLastCheckedTime();
  const categoryCounts = getCategoryCounts();
  const todayChangeIds = getTodayChangeIds();
  const todayTotalIds = getTodayTotalIds();

  return {
    stats,
    lastChecked,
    categoryCounts,
    profile,
    todayChangeIds,
    todayTotalIds
  };
};

