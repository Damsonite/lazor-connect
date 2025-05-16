export interface ContactBase {
  first_name: string;
  last_name: string;
  birthday?: string;
  email?: string;
  phone_numbers?: string[];
  addresses?: string[];
  social_profiles?: string[];
  company?: string;
  job_title?: string;
  contact_type?: string;
  notes?: string;
  favorite?: boolean;
  tags: string[];
}

export interface Contact extends ContactBase {
  id: number;
}

export interface ContactCreate extends ContactBase {}
