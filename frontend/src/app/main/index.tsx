import { useRouter } from "expo-router";
import { Text, TouchableOpacity, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { font } from "../../shared/designSystem";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/listOfDoctors")}>
        <Text
          style={{
            color: "#6d2828",
            fontSize: font.m,
            fontWeight: "500",
          }}
        >
          {'Go to the "CONSULTATIONS" screen'}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/appointments")}>
        <Text
          style={{
            color: "#6d2828",
            fontSize: font.m,
            fontWeight: "500",
          }}
        >
          {'Go to the "APPOINTMENTS" screen'}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/chats/")}>
        <Text
          style={{
            color: "#6d2828",
            fontSize: font.m,
            fontWeight: "500",
          }}
        >
          {'Go to the "CHATS" screen'}
        </Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  touchable: {
    width: "90%",
    paddingVertical: 16,
    borderRadius: 50,
    alignItems: "center",
    marginVertical: 8,
    backgroundColor: "#FFF8F8",
    borderWidth: 1.5,
    borderColor: "#FADADD",
  },
});
