import VideoUI from "@/src/components/video_ui";
import {
  Call,
  CallControls,
  CallingState,
  StreamCall,
  StreamVideo,
  StreamVideoClient,
  useCallStateHooks,
  User,
} from "@stream-io/video-react-native-sdk";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { Text } from "react-native";

const apiKey = "mmhfdzb5evj2";
const userId = "Ginger_Albatross";
const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3Byb250by5nZXRzdHJlYW0uaW8iLCJzdWIiOiJ1c2VyL0dpbmdlcl9BbGJhdHJvc3MiLCJ1c2VyX2lkIjoiR2luZ2VyX0FsYmF0cm9zcyIsInZhbGlkaXR5X2luX3NlY29uZHMiOjYwNDgwMCwiaWF0IjoxNzY0MzM2ODQwLCJleHAiOjE3NjQ5NDE2NDB9.gQmz8X1oOYq4pJ8YGHVx5PQlsPsiGqC12D9VFRxUc10";
const callId = "o4M0r3gWGHoGjjW6yqoFd";
const user: User = { id: userId };

export default function VideoCallScreen() {
  const [client, setClient] = useState<StreamVideoClient | null>(null);
  const [call, setCall] = useState<Call | null>(null);

  const router = useRouter();

  useEffect(() => {
    const streamClient = StreamVideoClient.getOrCreateInstance({ apiKey, user, token });
    const streamCall = streamClient.call("default", callId);
    streamCall.join({ create: true });

    setClient(streamClient);
    setCall(streamCall);
  }, []);

  if (!client || !call) {
    return <Text>Loading...</Text>;
  }

  const onHangup = async (): Promise<void> => {
    await call?.leave();
    router.back();
  };

  return (
    <StreamVideo client={client}>
      <StreamCall call={call}>
        <VideoUI />
        <CallControls onHangupCallHandler={onHangup} />
      </StreamCall>
    </StreamVideo>
  );
}
