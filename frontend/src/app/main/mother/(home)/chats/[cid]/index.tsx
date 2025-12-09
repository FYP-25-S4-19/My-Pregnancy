import useChatStore from "@/src/shared/chatStore";
import { useLocalSearchParams } from "expo-router";
import { Text, View } from "react-native";

export default function IndividualChatScreen() {
  const { cid } = useLocalSearchParams();
  const channelID = cid as string;
  const channel = useChatStore((state) => state.channel);

  return (
    <View>
      <Text>Individual Chat Screen - Channel ID: {channelID}</Text>
    </View>
  );
}
