import { Tabs } from "expo-router";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { colors, font } from "@/src/shared/designSystem";

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
        name="(home)"
        options={{
          title: "Home",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="home" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="recipe"
        options={{
          title: "Recipe",
          tabBarIcon: ({ color, size = 24 }) => (
            <MaterialCommunityIcons name="food-fork-drink" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="appointment"
        options={{
          title: "Appointment",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="calendar" size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color, size = 24 }) => <MaterialCommunityIcons name="human" size={size} color={color} />,
        }}
      />

      {/*<Tabs.Screen name="appointments" options={{ href: null }} />*/}
      {/*<Tabs.Screen name="appointments/[id]/" options={{ href: null }} />*/}
      {/*<Tabs.Screen name="chats/[id]" options={{ href: null }} />
      <Tabs.Screen name="journal/journal" options={{ href: null }} />*/}
    </Tabs>
  );
}
