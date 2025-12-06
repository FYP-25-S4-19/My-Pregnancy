import { BottomTabNavigationOptions } from "@react-navigation/bottom-tabs";
import { colors, font } from "./designSystem";

export const TAB_BAR_ICON_SIZE = 24;

export const tabScreenOptions: BottomTabNavigationOptions = {
  headerShown: false,
  tabBarActiveTintColor: colors.primary,
  tabBarInactiveTintColor: colors.tabIcon,
  tabBarLabelStyle: {
    fontSize: font.xs,
    fontWeight: "600",
    // marginTop: -8,
  },
  tabBarStyle: {
    paddingTop: 8,
    // paddingBottom: sizes.m,
    borderTopWidth: 1,
    borderTopColor: colors.lightGray,
    backgroundColor: "#fff",
  },
};
