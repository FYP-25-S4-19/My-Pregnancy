import { Dimensions } from "react-native";
const { width, height } = Dimensions.get("window");

export const COLORS = {
  primary: "#007AFF",
  secondary: "#5856D6",
  background: "#FFFFFF",
  surface: "#F2F2F7",
  textPrimary: "#000000",
  success: "#34C759",
  danger: "#FF3B30",
  border: "#D1D1D6",
};

const SPACING_UNIT = 8;

export const SIZES = {
  // Spacing
  xs: SPACING_UNIT * 0.5, // 4
  s: SPACING_UNIT * 1, // 8
  m: SPACING_UNIT * 2, // 16
  l: SPACING_UNIT * 3, // 24
  xl: SPACING_UNIT * 4, // 32

  // Typography
  fontBody: 16,
  fontH1: 24,
  fontH2: 20,
  fontCaption: 12,

  // Component
  borderRadius: 8,
  icon: 24,
  // Screen dimensions
  screenWidth: width,
  screenHeight: height,
};

export const FONTS = {
  regular: "System",
  medium: "System-Medium",
  bold: "System-Bold",
};

// ... export all constants
export default {
  COLORS,
  SIZES,
  FONTS,
  // ... other groups
};
