import { api } from "@/src/constants/api";
import { useRouter } from "expo-router";
import React, { useEffect } from "react";
import { ImageBackground, StatusBar, StyleSheet, Text, TouchableOpacity, View } from "react-native";

const image = require("../../../assets/images/wallpaper.jpg");

export default function IntroScreen() {
  const router = useRouter();

  useEffect(() => {
    console.log("The BaseURI is: ", api.getUri());
    api.get("/").then((res) => {
      console.log("Ping response data: ", res.data);
    });
  }, []);

  return (
    <ImageBackground source={image} style={styles.background} resizeMode="cover">
      <StatusBar barStyle="dark-content" />
      <View style={styles.container}>
        {/* App Title */}
        <View style={styles.titleContainer}>
          <View>
            <Text style={styles.titleLarge}>Track Baby's</Text>
            <Text style={styles.titleLarge}>Growth</Text>
          </View>
          <Text style={styles.titleSmall}>Week-by-week milestones & tips</Text>
        </View>
        <TouchableOpacity style={{ marginTop: 20 }} onPress={() => router.push("/(intro)/preregister")}>
          <Text>Continue as guest →</Text>
        </TouchableOpacity>
        <TouchableOpacity style={{ marginTop: 20 }} onPress={() => router.push("/appointments/video_call")}>
          <Text>DEBUG: Test Video Call Screen</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  titleContainer: {
    alignItems: "center",
    marginBottom: 80, // Space between title and question
    gap: 4,
  },
  titleSmall: {
    fontSize: 24,
    color: "#6d2828",
    // For a cursive font, you would load a custom font with Expo Font
    // fontFamily: 'YourCursiveFont',
    lineHeight: 26,
  },
  titleLarge: {
    fontSize: 40,
    fontWeight: "bold",
    color: "#6d2828",
    // For a rounded, bold font, you would load a custom font
    // fontFamily: 'YourRoundedBoldFont',
  },
  questionText: {
    fontSize: 18,
    color: "#6d2828",
    marginBottom: 30, // Space between question and first button
  },
  button: {
    width: "90%",
    paddingVertical: 16,
    borderRadius: 50, // This creates the pill shape
    alignItems: "center",
    marginVertical: 8,
  },
  primaryButton: {
    backgroundColor: "#FADADD", // A soft pink color
  },
  primaryButtonText: {
    color: "#6d2828",
    fontSize: 16,
    fontWeight: "500",
  },
  secondaryButton: {
    backgroundColor: "#FFF8F8", // A very light, almost white pink
    borderWidth: 1.5,
    borderColor: "#FADADD",
  },
  secondaryButtonText: {
    color: "#6d2828",
    fontSize: 16,
    fontWeight: "500",
  },
  adminLogin: {
    marginTop: 20, // Space above the admin login link
  },
  adminLoginText: {
    fontSize: 14,
    color: "#6d2828",
  },
});
