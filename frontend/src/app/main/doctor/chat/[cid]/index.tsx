import { Channel, MessageInput, MessageList, useChatContext } from "stream-chat-expo";
import { ActivityIndicator, Text, View, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { colors, font } from "@/src/shared/designSystem";
import { useLocalSearchParams } from "expo-router";

export default function IndividualChatScreen() {
  const { cid } = useLocalSearchParams();
  const { client } = useChatContext();
  const [channelType, channelID] = (cid as string)?.split(":") || [null, null];

  if (!client || !channelType || !channelID) {
    return (
      <View>
        {!client && <Text>Client is invalid</Text>}
        {!channelType && <Text>ChannelType is invalid</Text>}
        {!channelID && <Text>ChannelID is invalid</Text>}
        <ActivityIndicator />
      </View>
    );
  }

  const channel = client.channel(channelType, channelID);
  return (
    <SafeAreaView style={styles.container}>
      {/*<Text style={styles.headerText}>Dr John</Text>*/}
      <Channel channel={channel}>
        <MessageList />
        <MessageInput />
      </Channel>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.background,
  },
  headerText: {
    // paddingTop: sizes.l,
    fontSize: font.xl,
    fontWeight: "700",
    color: colors.text,
    textAlign: "center",
  },
});
