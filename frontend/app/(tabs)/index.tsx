import React from 'react';
import{
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ImageBackground,
  StatusBar
} from 'react-native';

const image = require('../../assets/images/wallpaper.jpg');

export default function HomeScreen() {
  return (
    <ImageBackground 
      source={image} 
      style={styles.background}
      resizeMode="cover"
    >
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
          onPress={() => console.log('Mom-to-be selected')}
        >
          <Text style={styles.primaryButtonText}>I'm a Mom-to-be</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.button, styles.secondaryButton]}
          onPress={() => console.log('Specialist selected')}
        >
          <Text style={styles.secondaryButtonText}>I'm a Specialist</Text>
        </TouchableOpacity>

        {/* Admin Login Link */}
        <TouchableOpacity 
          style={styles.adminLogin}
          onPress={() => console.log('Admin Login pressed')}
        >
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
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  titleContainer: {
    alignItems: 'center',
    marginBottom: 80, // Space between title and question
  },
  titleSmall: {
    fontSize: 24,
    color: '#6d2828',
    // For a cursive font, you would load a custom font with Expo Font
    // fontFamily: 'YourCursiveFont', 
    lineHeight: 26,
  },
  titleLarge: {
    fontSize: 40,
    fontWeight: 'bold',
    color: '#6d2828',
    // For a rounded, bold font, you would load a custom font
    // fontFamily: 'YourRoundedBoldFont', 
  },
  questionText: {
    fontSize: 18,
    color: '#6d2828',
    marginBottom: 30, // Space between question and first button
  },
  button: {
    width: '90%',
    paddingVertical: 16,
    borderRadius: 50, // This creates the pill shape
    alignItems: 'center',
    marginVertical: 8,
  },
  primaryButton: {
    backgroundColor: '#FADADD', // A soft pink color
  },
  primaryButtonText: {
    color: '#6d2828',
    fontSize: 16,
    fontWeight: '500',
  },
  secondaryButton: {
    backgroundColor: '#FFF8F8', // A very light, almost white pink
    borderWidth: 1.5,
    borderColor: '#FADADD',
  },
  secondaryButtonText: {
    color: '#6d2828',
    fontSize: 16,
    fontWeight: '500',
  },
  adminLogin: {
    marginTop: 20, // Space above the admin login link
  },
  adminLoginText: {
    fontSize: 14,
    color: '#6d2828',
  },
});