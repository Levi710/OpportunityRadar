import { getSourceStats, getLastCheckedTime, getCategoryCounts, getStudentProfile, getTodayChangeIds, getTodayTotalIds } from '$lib/db';

export const load: LayoutServerLoad = () => {
  const stats = getSourceStats();
  const lastChecked = getLastCheckedTime();
  const categoryCounts = getCategoryCounts();
  const profile = getStudentProfile();
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
