import React from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { Text, StyleSheet } from "react-native";
import { colors, font, sizes } from "@/src/shared/designSystem";

interface ChatData {
  id: string;
  doctor_id: string;
  doctor_name: string;
  last_message: string;
  unread_count: number;
  avatar_url: string | null;
}

export default function MotherChatListScreen() {
  // const [searchQuery, setSearchQuery] = useState<string>("");
  // const [activeFilter, setActiveFilter] = useState<"all" | "unread">("all");

  // const { data } = useQuery({});

  // const filteredChats = data?.filter((chat) => {
  //   const matchesSearch = chat.doctor_name.toLowerCase().includes(searchQuery.toLowerCase());
  //   const matchesFilter = activeFilter === "all" || (activeFilter === "unread" && chat.unread_count > 0);
  //   return matchesSearch && matchesFilter;
  // });

  return (
    <SafeAreaView edges={["top"]}>
      <Text>Mother Chat Screen - TODO: Show list of doctors that you are chatting with</Text>
    </SafeAreaView>
    // <SafeAreaView style={styles.container} edges={["top"]}>
    //   <ScrollView showsVerticalScrollIndicator={false}>
    //     {/* Header */}
    //     <View style={styles.header}>
    //       <Text style={styles.headerTitle}>Chats</Text>
    //     </View>

    //     {/* Search Bar */}
    //     <View style={styles.searchContainer}>
    //       <SearchBar value={searchQuery} onChangeText={setSearchQuery} placeholder="Search" />
    //     </View>

    //     {/* Filter Buttons */}
    //     <View style={styles.filterContainer}>
    //       <FilterButton label="All" isActive={activeFilter === "all"} onPress={() => setActiveFilter("all")} />
    //       <FilterButton label="Unread" isActive={activeFilter === "unread"} onPress={() => setActiveFilter("unread")} />
    //     </View>

    //     {/* Chat List */}
    //     <View style={styles.chatList}>
    //       {filteredChats && filteredChats.length > 0 ? (
    //         filteredChats.map((chat) => (
    //           <ChatItem
    //             key={chat.id}
    //             id={chat.id}
    //             doctorName={chat.doctor_name}
    //             lastMessage={chat.last_message}
    //             unreadCount={chat.unread_count}
    //             avatarUrl={chat.avatar_url}
    //             onPress={() => router.push(`/main/chats/${chat.doctor_id}/`)}
    //           />
    //         ))
    //       ) : (
    //         <View style={styles.emptyContainer}>
    //           <Text style={styles.emptyText}>No chats yet</Text>
    //         </View>
    //       )}
    //     </View>
    //   </ScrollView>
    // </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: sizes.l,
    paddingTop: sizes.m,
    paddingBottom: sizes.m,
  },
  headerTitle: {
    fontSize: font.xxl,
    fontWeight: "700",
    color: colors.text,
  },
  searchContainer: {
    marginBottom: sizes.m,
  },
  filterContainer: {
    flexDirection: "row",
    paddingHorizontal: sizes.l,
    gap: sizes.s,
    marginBottom: sizes.m,
  },
  chatList: {
    flex: 1,
  },
  emptyContainer: {
    paddingVertical: sizes.xxl,
    alignItems: "center",
  },
  emptyText: {
    fontSize: font.m,
    color: colors.tabIcon,
    fontWeight: "500",
  },
});
