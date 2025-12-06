import { useRouter } from "expo-router";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
// import { View } from "react-native-safe-area-context";
//
import useAuthStore from "@/src/shared/authStore";

export default function MotherHomeScreen() {
  const router = useRouter();
  const me = useAuthStore((state) => state.me);

  return (
    <View>
      <Text>Mother home screen</Text>
    </View>
    // <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
    //   <Text
    //     style={{
    //       fontSize: font.l,
    //       fontWeight: "600",
    //       marginBottom: sizes.m,
    //     }}
    //   >
    //     Logged in as a {me?.role.toLowerCase()}
    //   </Text>

    //   <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/mother/listOfDoctors")}>
    //     <Text
    //       style={{
    //         color: "#6d2828",
    //         fontSize: font.m,
    //         fontWeight: "500",
    //       }}
    //     >
    //       {'Go to the "CONSULTATIONS" screen'}
    //     </Text>
    //   </TouchableOpacity>
    //   <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/mother/appointments")}>
    //     <Text
    //       style={{
    //         color: "#6d2828",
    //         fontSize: font.m,
    //         fontWeight: "500",
    //       }}
    //     >
    //       {'Go to the "APPOINTMENTS" screen'}
    //     </Text>
    //   </TouchableOpacity>
    //   <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/mother/journal/journal")}>
    //     <Text
    //       style={{
    //         color: "#6d2828",
    //         fontSize: font.m,
    //         fontWeight: "500",
    //       }}
    //     >
    //       {'Go to the "JOURNAL" screen'}
    //     </Text>
    //   </TouchableOpacity>
    //   <TouchableOpacity style={styles.touchable} onPress={() => router.push("/main/mother/chats")}>
    //     <Text
    //       style={{
    //         color: "#6d2828",
    //         fontSize: font.m,
    //         fontWeight: "500",
    //       }}
    //     >
    //       {'Go to the "CHATS" screen'}
    //     </Text>
    //   </TouchableOpacity>
    // </View>
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
