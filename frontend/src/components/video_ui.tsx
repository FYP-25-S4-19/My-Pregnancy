import { useCallStateHooks, CallParticipantsList } from "@stream-io/video-react-native-sdk";

export default function VideoUI() {
  const { useParticipants } = useCallStateHooks();
  const participants = useParticipants();

  return <CallParticipantsList participants={participants} />;
}
