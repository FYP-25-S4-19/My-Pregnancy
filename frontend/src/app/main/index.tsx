import api from "@/src/constants/api";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "expo-router";
import { FlatList, Text, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

interface AppointmentData {
  appointment_id: number;
  doctor_id: number;
  doctor_name: string;
  mother_id: number;
  mother_name: string;
  start_time: string;
  status: string;
}

export default function HomeScreen() {
  const router = useRouter();

  const query = useQuery({
    queryKey: ["Video Calls"],
    queryFn: async (): Promise<AppointmentData[]> => {
      const res = await api.get("/appointments/");
      return res.data;
    },
  });

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <FlatList
        data={query.data}
        keyExtractor={(appt) => appt.appointment_id.toString()}
        renderItem={({ item }) => {
          return (
            <TouchableOpacity
              style={{ padding: 10, borderBottomWidth: 1, borderBottomColor: "#ccc" }}
              onPress={() => router.push(`/appointments/${item.appointment_id.toString()}/video_call`)}
            >
              <Text>
                Appointment with Dr. {item.doctor_name} at {new Date(item.start_time).toLocaleString()}
              </Text>
            </TouchableOpacity>
          );
        }}
      />
    </SafeAreaView>
  );
}
