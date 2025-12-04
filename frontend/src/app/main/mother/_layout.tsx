import { Tabs } from "expo-router";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { colors, font, sizes } from "@/src/shared/designSystem";

export default function MotherTabLayout() {
  return (
    <Tabs
      screenOptions={{
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
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="home" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="listOfDoctors"
        options={{
          title: "Doctors",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="home" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="appointments"
        options={{
          title: "Appointments",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="calendar" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="chats"
        options={{
          title: "Chat",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="chat" size={size} color={color} />,
        }}
      />

      {/*<Tabs.Screen name="appointments" options={{ href: null }} />*/}
      {/*<Tabs.Screen name="appointments/[id]/" options={{ href: null }} />*/}
      <Tabs.Screen name="chats/[id]" options={{ href: null }} />
    </Tabs>
  );
}
