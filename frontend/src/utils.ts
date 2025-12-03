import { jwtDecode } from "jwt-decode";

const utils = {
  invalidOrExpiredJWT(jwt: string): boolean {
    try {
      const decoded: { exp: number } = jwtDecode(jwt);
      const currentTime = Math.floor(Date.now() / 1000);
      return decoded.exp < currentTime;
    } catch (_) {
      return false;
    }
  },
};

export default utils;
