export interface Source {
  id: number;
  name: string;
  url: string;
  css_selector: string;
  is_js_rendered: number;
  active: number;
  category: string;
  tags: string; // JSON string in DB
  created_at: string;
}

export interface Snapshot {
  id: number;
  source_id: number;
  content_hash: string;
  raw_content: string | null;
  checked_at: string;
  changed: number;
}

export interface ChangeEvent {
  id: number;
  source_name: string;
  source_url: string;
  category: string;
  checked_at: string;
  raw_content: string | null;
}

export interface SourceWithStats extends Source {
  last_checked: string | null;
  last_changed: string | null;
}

export interface SourceStats {
  total: number;
  active: number;
  changed_today: number;
}

export interface StudentProfile {
  id?: number;
  email: string;
  name: string;
  branch: string;
  year: number;
  college: string;
  verified?: boolean;
}
