import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { useStreamSetup } from "../shared/hooks/useStreamSetup";
import { Chat, OverlayProvider } from "stream-chat-expo";
import useAuthStore from "../shared/authStore";
import { Stack } from "expo-router";
import utils from "../shared/utils";
import { useEffect } from "react";
import "react-native-reanimated";

const useRemoveAccessTokenFromStoreIfInvalid = () => {
  const isHydrated = useAuthStore.persist.hasHydrated();
  const accessToken = useAuthStore((state) => state.accessToken);
  const clearAuthState = useAuthStore((state) => state.clearAuthState);

  useEffect(() => {
    if (!isHydrated) {
      return;
    }
    if (!accessToken) {
      return;
    }

    const decodedToken = utils.safeDecodeUnexpiredJWT(accessToken);
    const isTokenInvalid = decodedToken === null;

    if (isTokenInvalid) {
      console.log("Access token is invalid or expired, clearing auth state");
      clearAuthState();
    }
  }, [isHydrated, accessToken, clearAuthState]);
};

const queryClient = new QueryClient();

export default function RootLayout() {
  useRemoveAccessTokenFromStoreIfInvalid();
  const { chatClient, isReady } = useStreamSetup();

  if (chatClient && isReady) {
    return (
      <GestureHandlerRootView>
        <OverlayProvider>
          <QueryClientProvider client={queryClient}>
            <Chat client={chatClient}>
              <Stack screenOptions={{ headerShown: false }} />
            </Chat>
          </QueryClientProvider>
        </OverlayProvider>
      </GestureHandlerRootView>
    );
  }
  return (
    <GestureHandlerRootView>
      <OverlayProvider>
        <QueryClientProvider client={queryClient}>
          <Stack screenOptions={{ headerShown: false }} />
        </QueryClientProvider>
      </OverlayProvider>
    </GestureHandlerRootView>
  );
}
