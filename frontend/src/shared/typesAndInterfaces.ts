export interface MeData {
  id: number;
  email: string;
  first_name: string;
  middle_name: string | null;
  last_name: string;
  role: string;
}

export interface JwtData {
  exp: number;
  sub: string;
}
