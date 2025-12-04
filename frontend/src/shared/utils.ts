import { jwtDecode } from "jwt-decode";
import { JwtData } from "./typesAndInterfaces";

const utils = {
  /**
   * Will try to decode the JWT and return null if it FAILS or if is EXPIRED
   */
  safeDecodeUnexpiredJWT(jwt: string): JwtData | null {
    try {
      const jwtData = jwtDecode<JwtData>(jwt);
      return jwtData.exp < Math.floor(Date.now() / 1000) ? null : jwtData;
    } catch {
      return null;
    }
  },
};

export default utils;
