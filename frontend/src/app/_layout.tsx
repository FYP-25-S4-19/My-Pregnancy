import { Router, Slot, Stack, usePathname, useRouter } from "expo-router";
import useAuthStore from "../stores/authStore";
import { useEffect } from "react";
import "react-native-reanimated";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const useAuthRedirect = () => {
  const router: Router = useRouter();
  const pathname: string = usePathname();
  const { accessToken } = useAuthStore();
  const isHydrated: boolean = useAuthStore.persist.hasHydrated();

  useEffect(() => {
    if (!isHydrated) {
      return;
    }

    const isTokenValid: boolean = !!accessToken;
    if (!isTokenValid) {
      router.replace("/");
    }

    router.replace("/main");
  }, [isHydrated, accessToken, pathname, router]);
};

const queryClient = new QueryClient();

export default function RootLayout() {
  // useAuthRedirect();
  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }} />
    </QueryClientProvider>
  );
}
