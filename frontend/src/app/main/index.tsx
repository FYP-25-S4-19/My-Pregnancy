import { useRouter } from "expo-router";
import { Text, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <TouchableOpacity
        style={{
          width: "90%",
          paddingVertical: 16,
          borderRadius: 50, // This creates the pill shape
          alignItems: "center",
          marginVertical: 8,
          backgroundColor: "#FFF8F8", // A very light, almost white pink
          borderWidth: 1.5,
          borderColor: "#FADADD",
        }}
        onPress={() => router.push("/main/consultations")}
      >
        <Text
          style={{
            color: "#6d2828",
            fontSize: 16,
            fontWeight: "500",
          }}
        >
          {'Go to the "CONSULTATIONS" screen'}
        </Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
