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
import { useEffect, useState } from "react";
import { Text, View, ActivityIndicator } from "react-native";

interface StreamApiResponse {
  token: string;
  api_key: string;
  user_id: string;
}

export default function VideoCallScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();

  const [client, setClient] = useState<StreamVideoClient | null>(null);
  const [call, setCall] = useState<Call | null>(null);
  const [streamApiData, setStreamApiData] = useState<StreamApiResponse | null>(null);

  const me = useAuthStore((state) => state.me);

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const res = await api.get("/stream/token");
        const data = res.data as StreamApiResponse;
        setStreamApiData(data);
      } catch (error) {
        console.error("Error fetching stream token:", error);
      }
    };
    fetchToken();
  }, []);

  useEffect(() => {
    if (!me || !id || !streamApiData) return;

    const apiKey = String(process.env.EXPO_PUBLIC_STREAM_API_KEY);
    const user: User = { id: me.id.toString() };
    const newClient = StreamVideoClient.getOrCreateInstance({ apiKey, user, token: streamApiData.token });
    const newCall = newClient.call("default", id.toString());

    const joinCall = async () => {
      try {
        await newCall.join({ create: true });
        setClient(newClient);
        setCall(newCall);
      } catch (error) {
        console.error("Error joining call:", error);
      }
    };
    joinCall();

    return () => {
      newCall.leave().catch((err) => console.error("Error leaving call", err));
      newClient.disconnectUser().catch((err) => console.error("Error disconnecting", err));

      setClient(null);
      setCall(null);
    };
  }, [me, id, streamApiData]);

  if (!client || !call) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" />
        <Text>Joining Call...</Text>
      </View>
    );
  }

  return (
    <StreamVideo client={client}>
      <StreamCall call={call}>
        <VideoUI />
        <CallControls
          onHangupCallHandler={async () => {
            router.back();
          }}
        />
      </StreamCall>
    </StreamVideo>
  );
}
