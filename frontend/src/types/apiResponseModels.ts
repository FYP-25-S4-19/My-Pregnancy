export interface AppointmentData {
  appointment_id: number;
  doctor_id: number;
  doctor_name: string;
  mother_id: number;
  mother_name: string;
  start_time: string;
  status: string;
}

export interface StreamApiResponse {
  token: string;
  api_key: string;
  user_id: string;
}

export interface DoctorPreviewData {
  doctor_id: string;
  profile_img_url: string | null;
  first_name: string;
  is_liked: boolean;
}
