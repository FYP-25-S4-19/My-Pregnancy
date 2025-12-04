// import { useLocalSearchParams } from "expo-router";
import { StreamChat } from "stream-chat";
import { View } from "react-native";
import { useEffect } from "react";
import useAuthStore from "@/src/shared/authStore";

export default function ChatScreen() {
  // const { id } = useLocalSearchParams();
  // const chatID: string = id;

  const streamClient = StreamChat.getInstance(String(process.env.EXPO_PUBLIC_STREAM_CHAT_API_KEY));
  const me = useAuthStore((state) => state.me);

  useEffect(() => {
    if (!me) return;

    const connectUserAsync = async (): Promise<void> => {
      try {
        await streamClient.connectUser(
          {
            id: String(me.id),
            name: [me.first_name, me.middle_name, me.last_name]
              .filter((namePart) => namePart && namePart.trim().length > 0)
              .join(" "),
          },
          "",
        );
      } catch {}
    };
    connectUserAsync();
    // await client.connectUser({}, "");
  }, [me, streamClient]);

  return <View></View>;
}
