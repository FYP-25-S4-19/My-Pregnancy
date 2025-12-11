import { TouchableOpacity, View, StyleSheet, Text } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { colors, font, sizes } from "../shared/designSystem";
import { useRouter } from "expo-router";

const ChatHeader = ({ title }: { title: string }) => {
  const router = useRouter();
  return (
    <View style={styles.headerContainer}>
      <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
        <MaterialCommunityIcons name="chevron-left" size={32} color={colors.text} />
      </TouchableOpacity>
      <Text style={styles.headerText}>{title}</Text>
      {/* Empty View to balance the center title */}
      <View style={{ width: 32 }} />
    </View>
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: sizes.m,
    paddingVertical: sizes.s,
    backgroundColor: colors.background,
  },
  backButton: {
    padding: sizes.xs,
  },
  headerText: {
    fontSize: font.xl,
    fontWeight: "700",
    color: colors.primary,
    textAlign: "center",
  },
});

export default ChatHeader;
