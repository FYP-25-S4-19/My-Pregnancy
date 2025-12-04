import useAuthStore from "@/src/shared/authStore";
import { RoleType } from "@/src/shared/typesAndInterfaces";
import { Redirect } from "expo-router";

export default function MainIndexScreen() {
  const role: RoleType | undefined = useAuthStore((state) => state.me?.role);

  if (role === "PREGNANT_WOMAN") {
    return <Redirect href="/main/mother" />;
  } else if (role === "VOLUNTEER_DOCTOR") {
    return <Redirect href="/main/doctor" />;
  } else if (role === "NUTRITIONIST") {
    return <Redirect href="/main/nutritionist" />;
  }
  return <Redirect href="/main/guest" />;
}
