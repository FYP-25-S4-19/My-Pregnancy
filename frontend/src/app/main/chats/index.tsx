import { useQuery } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import { View } from "react-native";

export default function ChatScreen() {
  const { isLoading, data } = useQuery({
    queryKey: ["consultations"],
  });

  return <View></View>;
}
