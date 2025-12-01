import axios from "axios";
import Constants from "expo-constants";
import { Platform } from "react-native";
import * as Device from "expo-device";
import useAuthStore from "../stores/authStore";

if (process.env.EXPO_PUBLIC_APP_ENV !== "dev" && process.env.EXPO_PUBLIC_APP_ENV !== "prod") {
  throw new Error("EXPO_PUBLIC_APP_ENV should be set to either 'dev' or 'prod' explicitly");
}

const getBaseUrl = () => {
  if (process.env.EXPO_PUBLIC_APP_ENV === "prod") {
    return "https://api.my-pregnancy.click/";
  }

  // EMULATOR CHECK: Device.isDevice returns 'false' if it's an emulator/simulator
  const isEmulator = !Device.isDevice;
  if (isEmulator) {
    if (Platform.OS === "android") {
      return "http://10.0.2.2:8000/"; // Android Emulator uses special localhost
    }
    return "http://localhost:8000/"; // iOS Simulator can use localhost
  }

  // PHYSICAL DEVICE (Dynamic IP Detection): We extract the IP address of your machine from the manifest
  const debuggerHost = Constants.expoConfig?.hostUri;
  const localhostIp = debuggerHost?.split(":")[0];
  if (localhostIp) {
    return `http://${localhostIp}:8000/`;
  }
  throw new Error("Could not determine API URL. Ensure you are running the development server.");
};

const api = axios.create({ baseURL: getBaseUrl() });

/**
 * Request interceptor to add Authorization header if access token is available
 */
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

/**
 * Response interceptor to handle 401 errors globally.
 * If a 401 error is encountered, the user is logged out.
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.log("Authentication error: Token expired or invalid.");
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  },
);

export default api;
