import Database from 'better-sqlite3';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { ChangeEvent, Source, SourceWithStats, SourceStats, StudentProfile } from './types';

// Resolve database path relative to the ui project root
const __dirname = dirname(fileURLToPath(import.meta.url));
const dbPath = process.env.DATABASE_PATH || resolve(__dirname, '..', '..', '..', 'opportunityradar.db');
const db = new Database(dbPath, { readonly: true });

export interface QueryOptions {
  limit?: number;
  category?: string;
  branch?: string;
  sinceUtc?: string;
}

export function getChanges(options: QueryOptions = {}): ChangeEvent[] {
  const { limit = 50, category, branch, sinceUtc } = options;
  
  let query = `
    SELECT 
      s.id,
      src.name as source_name,
      src.url as source_url,
      src.category,
      s.checked_at,
      s.raw_content
    FROM snapshots s
    JOIN sources src ON s.source_id = src.id
    WHERE s.changed = 1
  `;
  
  const params: any[] = [];
  
  if (category) {
    query += ` AND src.category = ?`;
    params.push(category);
  }
  
  if (sinceUtc) {
    query += ` AND s.checked_at >= ?`;
    params.push(sinceUtc);
  }
  
  if (branch) {
    // tags is stored as JSON string like ["cs", "it"]
    // We use LIKE for simplicity since it's a small dataset, or json_each if available
    query += ` AND (src.tags LIKE ? OR src.tags LIKE '%"all"%')`;
    params.push(`%"${branch}"%`);
  }
  
  query += ` ORDER BY s.checked_at DESC LIMIT ?`;
  params.push(limit);
  
  return db.prepare(query).all(...params) as ChangeEvent[];
}

export function getAllSources(): SourceWithStats[] {
  return db.prepare(`
    SELECT 
      src.*,
      (SELECT MAX(s.checked_at) FROM snapshots s WHERE s.source_id = src.id) as last_checked,
      (SELECT MAX(s.checked_at) FROM snapshots s WHERE s.source_id = src.id AND s.changed = 1) as last_changed
    FROM sources src
    ORDER BY src.name ASC
  `).all() as SourceWithStats[];
}

export function getSourceStats(): SourceStats {
  const total = (db.prepare('SELECT COUNT(*) as c FROM sources').get() as any).c;
  const active = (db.prepare('SELECT COUNT(*) as c FROM sources WHERE active = 1').get() as any).c;
  const changed_today = (db.prepare(`
    SELECT COUNT(*) as c FROM snapshots 
    WHERE changed = 1 AND checked_at >= date('now')
  `).get() as any).c;
  return { total, active, changed_today };
}

export function getCategoryCounts(): Record<string, number> {
  const rows = db.prepare(`
    SELECT src.category, COUNT(*) as count
    FROM snapshots s
    JOIN sources src ON s.source_id = src.id
    WHERE s.changed = 1 AND s.checked_at >= date('now')
    GROUP BY src.category
  `).all() as any[];
  
  const counts: Record<string, number> = {};
  rows.forEach(r => counts[r.category] = r.count);
  return counts;
}

export function getTodayChangeIds(): { id: number, category: string }[] {
  return db.prepare(`
    SELECT s.id, src.category
    FROM snapshots s
    JOIN sources src ON s.source_id = src.id
    WHERE s.changed = 1 AND s.checked_at >= date('now')
  `).all() as { id: number, category: string }[];
}

export function getTodayTotalIds(): number[] {
  return db.prepare(`
    SELECT id FROM snapshots 
    WHERE changed = 1 AND checked_at >= date('now')
  `).all().map((r: any) => r.id);
}

export function getStudentProfile(): StudentProfile | null {
  // For V2 we just get the first one as it's a local single-user system
  return db.prepare('SELECT * FROM student_profiles LIMIT 1').get() as StudentProfile || null;
}

export function upsertStudentProfile(profile: Omit<StudentProfile, 'id'>): void {
  // Use a writable connection for profile updates
  const writeDb = new Database(dbPath);
  try {
    writeDb.prepare(`
      INSERT INTO student_profiles (email, name, branch, year, college)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(email) DO UPDATE SET
      name=excluded.name, branch=excluded.branch, year=excluded.year, college=excluded.college
    `).run('user@local', profile.name, profile.branch, profile.year, profile.college);
  } finally {
    writeDb.close();
  }
}

export function getLastCheckedTime(): string | null {
  const row = db.prepare('SELECT MAX(checked_at) as t FROM snapshots').get() as any;
  return row?.t ?? null;
}
