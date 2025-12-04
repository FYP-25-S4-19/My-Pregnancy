import VideoUI from "@/src/components/VideoUI";
import {
  Call,
  CallControls,
  StreamCall,
  StreamVideo,
  StreamVideoClient,
  User,
} from "@stream-io/video-react-native-sdk";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useRef, useState } from "react";
import { Text, View, ActivityIndicator, StyleSheet } from "react-native";
import streamTokenProvider from "@/src/shared/streamTokenProvider";
import useAuthStore from "@/src/shared/authStore";

type InitState = "loading" | "ready" | "error";

export default function VideoCallScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const me = useAuthStore((state) => state.me);

  const [initState, setInitState] = useState<InitState>("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [client, setClient] = useState<StreamVideoClient | null>(null);
  const [call, setCall] = useState<Call | null>(null);

  const clientRef = useRef<StreamVideoClient | null>(null);
  const callRef = useRef<Call | null>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    isMountedRef.current = true;

    const initializeVideoCall = async () => {
      try {
        if (!me || !id) {
          throw new Error("Missing user or call ID");
        }

        const apiKey = process.env.EXPO_PUBLIC_STREAM_API_KEY;
        if (!apiKey) {
          throw new Error("Stream API key not configured");
        }

        const user: User = { id: me.id.toString() };
        const newClient = StreamVideoClient.getOrCreateInstance({
          apiKey,
          user,
          tokenProvider: streamTokenProvider,
        });

        clientRef.current = newClient;
        if (isMountedRef.current) {
          setClient(newClient);
        }

        // Create and join call
        const newCall = newClient.call("default", id.toString());
        callRef.current = newCall;

        await newCall.join({ create: true });

        if (isMountedRef.current) {
          setCall(newCall);
          setInitState("ready");
        }
      } catch (error) {
        console.error("Failed to initialize video call:", error);

        // Cleanup any partial state
        await cleanupResources();

        if (isMountedRef.current) {
          const message = error instanceof Error ? error.message : "Failed to join video call";
          setErrorMessage(message);
          setInitState("error");

          // Navigate back after a brief delay to show error
          setTimeout(() => {
            if (isMountedRef.current) {
              router.back();
            }
          }, 2000);
        }
      }
    };

    const cleanupResources = async () => {
      const errors: string[] = [];

      // Leave call if it exists
      if (callRef.current) {
        try {
          await callRef.current.leave();
        } catch (err) {
          errors.push(`Call leave error: ${err}`);
        }
        callRef.current = null;
      }

      // Disconnect client if it exists
      if (clientRef.current) {
        try {
          await clientRef.current.disconnectUser();
        } catch (err) {
          errors.push(`Client disconnect error: ${err}`);
        }
        clientRef.current = null;
      }

      if (errors.length > 0) {
        console.error("Cleanup errors:", errors.join(", "));
      }
    };

    initializeVideoCall();

    // Cleanup on unmount
    return () => {
      isMountedRef.current = false;
      cleanupResources();
    };
  }, [me, id, router]);

  if (initState === "loading") {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Joining call...</Text>
      </View>
    );
  }

  if (initState === "error") {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>❌ {errorMessage}</Text>
        <Text style={styles.errorSubtext}>Returning to previous screen...</Text>
      </View>
    );
  }

  // Ready state
  // This shouldn't happen if initState is "ready", but just in case
  if (!client || !call) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <StreamVideo client={client}>
      <StreamCall call={call}>
        <VideoUI />
        <CallControls
          onHangupCallHandler={async () => {
            router.back();
          }}
        />
      </StreamCall>
    </StreamVideo>
  );
}

const styles = StyleSheet.create({
  centerContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000",
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: "#FFF",
  },
  errorText: {
    fontSize: 18,
    color: "#FF3B30",
    fontWeight: "600",
    textAlign: "center",
    paddingHorizontal: 32,
  },
  errorSubtext: {
    marginTop: 12,
    fontSize: 14,
    color: "#8E8E93",
    textAlign: "center",
  },
});
