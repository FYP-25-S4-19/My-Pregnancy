import VideoUI from "@/src/components/video_ui";
import api from "@/src/constants/api";
import useAuthStore from "@/src/stores/authStore";
import {
  Call,
  CallControls,
  StreamCall,
  StreamVideo,
  StreamVideoClient,
  User,
} from "@stream-io/video-react-native-sdk";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useRef } from "react";
import { Text } from "react-native";

export default function VideoCallScreen() {
  const streamClient = useRef<StreamVideoClient | null>(null);
  const streamCall = useRef<Call | null>(null);

  const router = useRouter();

  const me = useAuthStore((state) => state.me);
  const streamToken = useAuthStore((state) => state.streamToken);
  const setStreamToken = useAuthStore((state) => state.setStreamToken);

  const { id } = useLocalSearchParams();

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const res = await api.get("/stream/token");
        setStreamToken(res.data.token);
      } catch (error) {
        console.error("Error fetching stream token:", error);
      }
    };
    fetchToken();
  }, [setStreamToken]);

  useEffect(() => {
    if (!me) {
      console.log("me is null....");
      return;
    }
    if (!streamToken) {
      console.log("No stream token...");
      return;
    }
    if (!id) {
      console.log("No id...");
      return;
    }

    const user = {
      id: me?.id.toString()!,
    } as User;
    const apiKey = String(process.env.EXPO_PUBLIC_STREAM_API_KEY);
    streamClient.current = StreamVideoClient.getOrCreateInstance({ apiKey, user, token: streamToken });

    try {
      console.log("Trying to join call....");
      streamCall.current = streamClient.current.call("default", id.toString());
      streamCall.current.join({ create: true });
      console.log("Finish try to join call....");
    } catch (error) {
      console.error("Error joining call:", error);
    }
  }, [streamToken, id, me]);

  if (!streamClient.current || !streamCall.current) {
    return <Text>Loading...</Text>;
  }

  return (
    <StreamVideo client={streamClient.current!}>
      <StreamCall call={streamCall.current!}>
        <VideoUI />
        <CallControls
          onHangupCallHandler={async (): Promise<void> => {
            await streamCall.current?.leave();
            router.back();
          }}
        />
      </StreamCall>
    </StreamVideo>
  );
}
