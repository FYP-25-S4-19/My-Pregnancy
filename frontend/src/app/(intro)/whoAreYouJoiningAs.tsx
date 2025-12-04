import React from "react";
import { ImageBackground, StatusBar, StyleSheet, Text, TouchableOpacity, View } from "react-native";

const image = require("../../../assets/images/wallpaper.jpg");

export default function WhoAreYouJoiningAsScreen() {
  return (
    <ImageBackground source={image} style={styles.background} resizeMode="cover">
      <StatusBar barStyle="dark-content" />
      <View style={styles.container}>
        {/* App Title */}
        <View style={styles.titleContainer}>
          <Text style={styles.titleSmall}>my</Text>
          <Text style={styles.titleLarge}>Pregnancy</Text>
        </View>

        {/* Role Selection Question */}
        <Text style={styles.questionText}>Who are you joining as?</Text>

        {/* Buttons */}
        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={() => console.log("Mom-to-be selected")}
        >
          <Text style={styles.primaryButtonText}>{"I'm a Mom-to-be"}</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={() => console.log("Specialist selected")}
        >
          <Text style={styles.secondaryButtonText}>{"I'm a Specialist"}</Text>
        </TouchableOpacity>

        {/* Admin Login Link */}
        <TouchableOpacity style={styles.adminLogin} onPress={() => console.log("Admin Login pressed")}>
          <Text style={styles.adminLoginText}>Admin Login →</Text>
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
    marginBottom: 80, 
  },
  titleSmall: {
    fontSize: 24,
    color: "#6d2828",
    
    lineHeight: 26,
  },
  titleLarge: {
    fontSize: 40,
    fontWeight: "bold",
    color: "#6d2828",
    
  },
  questionText: {
    fontSize: 18,
    color: "#6d2828",
    marginBottom: 30, 
  },
  button: {
    width: "90%",
    paddingVertical: 16,
    borderRadius: 50, 
    alignItems: "center",
    marginVertical: 8,
  },
  primaryButton: {
    backgroundColor: "#FADADD",
  },
  primaryButtonText: {
    color: "#6d2828",
    fontSize: 16,
    fontWeight: "500",
  },
  secondaryButton: {
    backgroundColor: "#FFF8F8", 
    borderWidth: 1.5,
    borderColor: "#FADADD",
  },
  secondaryButtonText: {
    color: "#6d2828",
    fontSize: 16,
    fontWeight: "500",
  },
  adminLogin: {
    marginTop: 20,
  },
  adminLoginText: {
    fontSize: 14,
    color: "#6d2828",
  },
});


