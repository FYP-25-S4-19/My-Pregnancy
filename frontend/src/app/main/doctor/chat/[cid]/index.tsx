import { Channel as ChannelElement, MessageInput, MessageList, useChatContext } from "stream-chat-expo";
import { ActivityIndicator, Text, View, KeyboardAvoidingView, Platform } from "react-native";
import ConsultationMessageFooter from "@/src/components/ConsultationMessageFooter";
import { SafeAreaView } from "react-native-safe-area-context";
import { chatStyles } from "@/src/shared/globalStyles";
import ChatHeader from "@/src/components/ChatHeader";
import { useLocalSearchParams } from "expo-router";
import useAuthStore from "@/src/shared/authStore";
import utils from "@/src/shared/utils";

export default function IndividualChatScreen() {
  const me = useAuthStore((state) => state.me);
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
  if (!me?.id) {
    return;
  }
  const mother = utils.getOtherMemberFromChannel(channel, me.id.toString());
  if (mother === undefined) {
    return;
  }
  const motherFirstName = mother.name?.split(" ")[0] || "Missing name wthelly";

  return (
    <SafeAreaView edges={["top", "left", "right"]}>
      <ChatHeader title={`${motherFirstName}`} />

      <ChannelElement channel={channel} MessageFooter={ConsultationMessageFooter}>
        <MessageList />

        <KeyboardAvoidingView keyboardVerticalOffset={Platform.OS === "ios" ? 10 : 0}>
          <View style={chatStyles.inputWrapper}>
            <MessageInput />
          </View>
        </KeyboardAvoidingView>
      </ChannelElement>
    </SafeAreaView>
  );
}
