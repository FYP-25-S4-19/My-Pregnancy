// import { Router, Stack, usePathname, useRouter } from "expo-router";
// import useAuthStore from "../stores/authStore";
// import { useEffect } from "react";
// import utils from "../utils";

import "react-native-reanimated";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";

// const useAuthRedirect = () => {
//   const router: Router = useRouter();
//   const pathname: string = usePathname();
//   const accessToken = useAuthStore((state) => state.accessToken);
//   const isHydrated: boolean = useAuthStore.persist.hasHydrated();

//   useEffect(() => {
//     if (!isHydrated) {
//       return;
//     }

//     const isTokenValid: boolean = !utils.invalidOrExpiredJWT(accessToken || "");

//     // Logged-out, but trying to access a auth-only page
//     // Redirect to the intro page
//     if (!isTokenValid && pathname !== "/") {
//       router.replace("/");
//     }

//     // Logged-in but just sitting in the intro page
//     // Redirect to the main page
//     if (isTokenValid && pathname === "/") {
//       router.replace("/main");
//     }
//   }, [isHydrated, accessToken, pathname, router]);
// };

const queryClient = new QueryClient();

export default function RootLayout() {
  // useAuthRedirect();
  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }} />
    </QueryClientProvider>
  );
}
