import axios from "axios";
import Constants from "expo-constants";
import { Platform } from "react-native";
import * as Device from "expo-device";

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
export const api = axios.create({ baseURL: getBaseUrl() });
