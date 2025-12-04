import React, { useRef, useState, useCallback, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  ImageBackground,
  Dimensions,
  StatusBar,
} from "react-native";
import { useRouter } from "expo-router";
import api from "@/src/constants/api";

const { width, height } = Dimensions.get("window");

/** ----- slide content ----- */
type Slide = {
  id: string;
  titleTop: string;      // e.g., "Track Baby's"
  titleBottom?: string;  // e.g., "Growth"
  subtitle: string;
  image: any;            // require(...)
};

const SLIDES: Slide[] = [
  {
    id: "track",
    titleTop: "Track Baby's",
    titleBottom: "Growth",
    subtitle: "Week-by-week milestones & tips.",
    image: require("../../../assets/images/onboarding/track.png"),
  },
  {
    id: "plan",
    titleTop: "Plan &",
    titleBottom: "Prepare",
    subtitle: "Checklists, reminders, and due-date calendar.",
    image: require("../../../assets/images/onboarding/plan.png"),
  },
  {
    id: "consult",
    titleTop: "Consult a",
    titleBottom: "Professional",
    subtitle: "Chat/video with a volunteer specialist.",
    image: require("../../../assets/images/onboarding/consult.png"),
  },
];

const WALLPAPER = require("../../../assets/images/wallpaper.jpg");

/** ----- palette ----- */
const MAROON = "#6d2828";
const PINK = "#FADADD";
const PINK_OUTLINE = "#f1cfd2";
const PAPER = "#FFF8F8";
const DOT_INACTIVE = "#e6c7cb";

/** ----- screen ----- */
export default function IntroPagerSinglePage() {
  const router = useRouter();
  const listRef = useRef<FlatList<Slide>>(null);
  const [index, setIndex] = useState(0);

  // keep your original ping
  useEffect(() => {
    try {
      console.log("BaseURI:", api.getUri());
      api.get("/").then((res) => console.log("Ping:", res.data));
    } catch {}
  }, []);

  const onViewableItemsChanged = useRef(({ viewableItems }: any) => {
    const i = viewableItems?.[0]?.index;
    if (typeof i === "number") setIndex(i);
  }).current;

  const viewabilityConfig = useRef({ viewAreaCoveragePercentThreshold: 60 }).current;

  const goPrev = useCallback(() => {
    if (index > 0) listRef.current?.scrollToIndex({ index: index - 1, animated: true });
  }, [index]);

  const goNext = useCallback(() => {
    if (index < SLIDES.length - 1) {
      listRef.current?.scrollToIndex({ index: index + 1, animated: true });
    }
  }, [index]);

  const renderItem = ({ item }: { item: Slide }) => (
    <View style={[styles.slide, { width }]}>
      {/* Title block (matches Figma proportions) */}
      <View style={styles.titleBlock}>
        <Text style={styles.titleTop}>{item.titleTop}</Text>
        {!!item.titleBottom && <Text style={styles.titleBottom}>{item.titleBottom}</Text>}
        <Text style={styles.subtitle}>{item.subtitle}</Text>
      </View>

      {/* Illustration with floating arrows close to it */}
      <View style={styles.heroArea}>
        <TouchableOpacity
          style={[styles.arrowCircle, index === 0 && styles.arrowDisabled]}
          onPress={goPrev}
          disabled={index === 0}
        >
          <Text style={styles.arrowText}>←</Text>
        </TouchableOpacity>

        <View style={styles.illustrationWrap}>
          {/* Note: if your PNG contains big whitespace, it will still look smaller.
             Re-export selection-only artwork to fix that perfectly. */}
          <Image source={item.image} resizeMode="contain" style={styles.illustration} />
        </View>

        <TouchableOpacity
          style={[
            styles.arrowCircle,
            index === SLIDES.length - 1 && styles.arrowDisabled,
          ]}
          onPress={goNext}
          disabled={index === SLIDES.length - 1}
        >
          <Text style={styles.arrowText}>→</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <ImageBackground source={WALLPAPER} style={styles.bg} resizeMode="cover">
      <StatusBar barStyle="dark-content" />
      <View style={styles.screen}>
        {/* Pager */}
        <FlatList
          ref={listRef}
          data={SLIDES}
          keyExtractor={(s) => s.id}
          renderItem={renderItem}
          horizontal
          pagingEnabled
          showsHorizontalScrollIndicator={false}
          onViewableItemsChanged={onViewableItemsChanged}
          viewabilityConfig={viewabilityConfig}
          getItemLayout={(_, i) => ({ length: width, offset: width * i, index: i })}
        />

        {/* Dots just above CTAs */}
        <View style={styles.dotsRow}>
          {SLIDES.map((_, i) => (
            <View key={i} style={[styles.dot, i === index && styles.dotActive]} />
          ))}
        </View>

        {/* CTAs */}
        <View style={styles.cta}>
          <TouchableOpacity
            style={[styles.btn, styles.btnFilled]}
            onPress={() => router.push("/(intro)/login")}
          >
            <Text style={styles.btnFilledText}>Login</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.btn, styles.btnOutline]}
            onPress={() => router.push("/(intro)/whoAreYouJoiningAs")}
          >
            <Text style={styles.btnOutlineText}>Register</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => router.push("/main")}>
            <Text style={styles.guest}>Continue as Guest →</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ImageBackground>
  );
}

/** ----- styles ----- */
const styles = StyleSheet.create({
  bg: { flex: 1 },
  screen: { flex: 1, justifyContent: "flex-start" },

  /* Slide area */
  slide: {
    paddingTop: height * 0.06,  // more top spacing like Figma
    paddingHorizontal: 20,
  },

  titleBlock: {
    alignItems: "center",
    justifyContent: "center",
  },
  titleTop: {
    fontSize: 24,
    color: MAROON,
    letterSpacing: 0.5,
    textTransform: "uppercase",
  },
  titleBottom: {
    fontSize: 40,
    fontWeight: "800",
    color: MAROON,
    textTransform: "uppercase",
    marginTop: 2,
  },
  subtitle: {
    marginTop: 8,
    fontSize: 13,
    color: MAROON,
    opacity: 0.9,
    textAlign: "center",
  },

  /* Illustration row with arrows hugging the image */
  heroArea: {
    marginTop: 10,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 10,
  },
  illustrationWrap: {
    width: width * 0.68,              // bigger hero like Figma
    height: Math.min(380, height * 0.42),
    alignItems: "center",
    justifyContent: "center",
  },
  illustration: {
    width: "100%",
    height: "100%",
  },
  arrowCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    borderWidth: 1.5,
    borderColor: PINK_OUTLINE,
    backgroundColor: PAPER,
    alignItems: "center",
    justifyContent: "center",
  },
  arrowDisabled: { opacity: 0.35 },
  arrowText: { fontSize: 20, color: MAROON, lineHeight: 20 },

  /* Dots & CTAs */
  dotsRow: {
    marginTop: 10,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: DOT_INACTIVE,
  },
  dotActive: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: MAROON,
  },

  cta: {
    alignItems: "center",
    paddingHorizontal: 20,
    paddingBottom: 28,
    marginTop: 12,
    gap: 12,
  },
  btn: {
    width: "88%",
    paddingVertical: 14,
    borderRadius: 28,
    alignItems: "center",
    justifyContent: "center",
  },
  btnFilled: { backgroundColor: PINK },
  btnFilledText: { color: MAROON, fontSize: 16, fontWeight: "700" },
  btnOutline: {
    backgroundColor: "transparent",
    borderWidth: 1.5,
    borderColor: PINK_OUTLINE,
  },
  btnOutlineText: { color: MAROON, fontSize: 16, fontWeight: "700" },
  guest: { color: MAROON, fontSize: 13, marginTop: 2 },
});