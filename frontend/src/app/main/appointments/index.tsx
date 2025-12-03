import api from "@/src/constants/api";
import useAuthStore from "@/src/stores/authStore";
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

export default function AppointmentsScreen() {
  const router = useRouter();
  const me = useAuthStore((state) => state.me);

  const { isLoading, data } = useQuery({
    queryKey: ["Video Calls"],
    queryFn: async (): Promise<AppointmentData[]> => {
      const res = await api.get("/appointments/");
      return res.data;
    },
  });

  if (isLoading) {
    return (
      <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <Text>Loading appointments...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      {data?.length === 0 ? (
        <Text>No appointments found.</Text>
      ) : (
        <FlatList
          data={data}
          keyExtractor={(appt) => appt.appointment_id.toString()}
          renderItem={({ item }) => {
            return (
              <TouchableOpacity
                style={{ padding: 10, borderBottomWidth: 1, borderBottomColor: "#ccc" }}
                onPress={() => router.push(`/main/appointments/${item.appointment_id.toString()}/video_call`)}
              >
                <Text>
                  {((): string => {
                    if (me?.role === "VOLUNTEER_DOCTOR") {
                      return `Appointment with ${item.mother_name} at ${new Date(item.start_time).toLocaleString()}`;
                    }
                    return `Appointment with Dr. ${item.doctor_name} at ${new Date(item.start_time).toLocaleString()}`;
                  })()}
                </Text>
              </TouchableOpacity>
            );
          }}
        />
      )}
    </SafeAreaView>
  );
}
