import useAuthStore from "./authStore";
import { jwtDecode } from "jwt-decode";
import utils from "./utils";
import { JwtData } from "./typesAndInterfaces";
import api from "./api";

interface StreamApiResponse {
  token: string;
}

/**
 * Feel free to call as often as possible. This function will cache the token
 * and only request a new one if the current token is expired or about to expire
 *
 * Will throw an error if the user is not authenticated or if the token fetch fails
 */
let cachedStreamToken: string | null = null;
const streamTokenProvider = async (): Promise<string> => {
  if (cachedStreamToken) {
    const decoded: any = jwtDecode(cachedStreamToken);
    const currentTime = Date.now() / 1000;
    if (decoded.exp > currentTime + 90) {
      return cachedStreamToken;
    }
  }

  try {
    const { accessToken } = useAuthStore.getState();
    if (!accessToken) {
      throw new Error("User not authenticated");
    }
    const jwt: JwtData | null = utils.safeDecodeUnexpiredJWT(accessToken);
    if (!jwt) {
      throw new Error("Invalid access token");
    }

    const res = await api.get("/stream/token");
    const data = res.data as StreamApiResponse;
    const streamToken: string = data.token;

    cachedStreamToken = streamToken;
    return streamToken;
  } catch (error) {
    console.error("Failed to fetch Stream token", error);
    throw error;
  }
};

export default streamTokenProvider;
