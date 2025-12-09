import { TAB_BAR_ICON_SIZE, tabScreenOptions } from "@/src/shared/globalStyles";
import { useStreamSetup } from "@/src/shared/hooks/useStreamSetup";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Tabs } from "expo-router";
import { ActivityIndicator } from "react-native";

export default function MotherTabLayout() {
  const { chatClient, isReady } = useStreamSetup();

  return (
    <Tabs screenOptions={tabScreenOptions}>
      <Tabs.Screen
        name="(home)"
        options={{
          title: "Home",
          tabBarIcon: ({ color, size = TAB_BAR_ICON_SIZE }) => (
            <MaterialCommunityIcons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="recipe"
        options={{
          title: "Recipe",
          tabBarIcon: ({ color, size = TAB_BAR_ICON_SIZE }) => (
            <MaterialCommunityIcons name="food-fork-drink" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="appointment"
        options={{
          title: "Appointment",
          tabBarIcon: ({ color, size = TAB_BAR_ICON_SIZE }) => (
            <MaterialCommunityIcons name="calendar" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color, size = TAB_BAR_ICON_SIZE }) => (
            <MaterialCommunityIcons name="human" size={size} color={color} />
          ),
        }}
      />

      {/*<Tabs.Screen name="appointments" options={{ href: null }} />*/}
      {/*<Tabs.Screen name="appointments/[id]/" options={{ href: null }} />*/}
      {/*<Tabs.Screen name="chats/[id]" options={{ href: null }} />
      <Tabs.Screen name="journal/journal" options={{ href: null }} />*/}
    </Tabs>
  );
}
