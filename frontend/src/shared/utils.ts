import { jwtDecode } from "jwt-decode";
import { JwtData, MeData } from "./typesAndInterfaces";

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
  formatFullname(me: MeData): string {
    return [me.first_name, me.middle_name, me.last_name]
      .filter((namePart) => namePart && namePart.trim().length > 0)
      .join(" ");
  },
};

export default utils;
