import React, { useState } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Platform,
  StatusBar,
} from 'react-native';


// --- CONFIGURATION ---
const COLORS = {
  primary: '#FF8A80', 
  secondary: '#FFCDD2', 
  background: '#FDFDFD',
  card: '#FFFFFF',
  text: '#5D4037', 
  textLight: '#A1887F',
  border: '#EF9A9A',
};


const Icon = ({ name, size, color }: { name: string; size: number; color: string }) => {
  let symbol = '?';
  if (name === 'chevron-left') symbol = '‹';
  if (name === 'chevron-right') symbol = '›';
  if (name === 'home') symbol = '🏠';
  if (name === 'book-open-variant') symbol = '📖';
  if (name === 'calendar-month') symbol = '📅';
  if (name === 'account') symbol = '👤';
  
  return <Text style={{ fontSize: size, color: color }}>{symbol}</Text>;
};


interface ChipProps {
  label: string;
  selected?: boolean;
  onPress: () => void;
}

interface VitalInputProps {
  label: string;
  unit: string;
  isDoubleInput?: boolean; // For Blood Pressure
}

// --- COMPONENTS ---

const Chip: React.FC<ChipProps> = ({ label, selected, onPress }) => {
  return (
    <TouchableOpacity
      style={[
        styles.chip,
        selected ? styles.chipSelected : styles.chipUnselected,
      ]}
      onPress={onPress}
    >
      <Text style={styles.chipText}>{label}</Text>
    </TouchableOpacity>
  );
};

// --- DATE UTILS ---
function formatDate(date: Date) {
  // Returns "Today, 14 October 2025" or "Monday, 13 October 2025"
  const today = new Date();
  const isToday =
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear();
  const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' };
  const formatted = date.toLocaleDateString(undefined, options);
  return isToday ? `Today, ${date.getDate()} ${date.toLocaleString('default', { month: 'long' })} ${date.getFullYear()}` : formatted;
}

function addDays(date: Date, days: number) {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

function dateKey(date: Date) {
  // "YYYY-MM-DD"
  return date.toISOString().slice(0, 10);
}

// 2. Vitals Row Component
const VitalRow: React.FC<VitalInputProps & { value: string | [string, string]; onChange: (v: any) => void }> = ({
  label,
  unit,
  isDoubleInput,
  value,
  onChange,
}) => (
  <View style={styles.vitalRow}>
    <Text style={styles.vitalLabel}>{label}</Text>
    <View style={styles.vitalInputContainer}>
      {isDoubleInput ? (
        <>
          <TextInput
            style={styles.vitalInputSmall}
            keyboardType="numeric"
            value={Array.isArray(value) ? value[0] : ''}
            onChangeText={(t) => onChange([t, Array.isArray(value) ? value[1] : ''])}
          />
          <Text style={styles.slashText}>/</Text>
          <TextInput
            style={styles.vitalInputSmall}
            keyboardType="numeric"
            value={Array.isArray(value) ? value[1] : ''}
            onChangeText={(t) => onChange([Array.isArray(value) ? value[0] : '', t])}
          />
        </>
      ) : (
        <TextInput
          style={styles.vitalInput}
          keyboardType="numeric"
          value={typeof value === 'string' ? value : ''}
          onChangeText={onChange}
        />
      )}
      {unit ? <Text style={styles.unitText}>{unit}</Text> : null}
    </View>
  </View>
);

export default function App() {
  // --- DATE STATE ---
  const [currentDate, setCurrentDate] = useState(new Date());
  const [activeTab, setActiveTab] = useState<'Journal' | 'Kicks'>('Journal');

  // --- JOURNAL DATA STATE ---
  type JournalData = {
    feeling: string;
    moods: string[];
    symptoms: string[];
    vitals: {
      bloodPressure: [string, string];
      sugar: string;
      heartRate: string;
      weight: string;
    };
  };
  const moods = [
    'Calm', 'Happy', 'Energetic', 'Sad', 'Anxious', 'Low Energy', 'Depressed', 'Confused', 'Irritated'
  ];
  const symptoms = [
    'Everything is fine', 'Cramps', 'Tender breasts', 'Headache', 'Cravings', 'Insomnia'
  ];

  // Store all data by date
  const [journals, setJournals] = useState<{ [date: string]: JournalData }>({});

  // Ensure journal exists for current date infinitely rendering
  const currentKey = dateKey(currentDate);
  React.useEffect(() => {
    if (!journals[currentKey]) {
      setJournals((prev) => ({
        ...prev,
        [currentKey]: {
          feeling: '',
          moods: [],
          symptoms: [],
          vitals: {
            bloodPressure: ['', ''],
            sugar: '',
            heartRate: '',
            weight: '',
          },
        },
      }));
    }
  }, [currentKey]);

  const journal = journals[currentKey] || {
    feeling: '',
    moods: [],
    symptoms: [],
    vitals: {
      bloodPressure: ['', ''],
      sugar: '',
      heartRate: '',
      weight: '',
    },
  };

  const handleDateChange = (direction: 'prev' | 'next') => {
    setCurrentDate((prev) => addDays(prev, direction === 'next' ? 1 : -1));
  };

  const handleFeelingChange = (text: string) => {
    setJournals((prev) => ({
      ...prev,
      [currentKey]: {
        ...journal,
        feeling: text,
      },
    }));
  };

  const setSelectedMoods = (newMoods: string[]) => {
    setJournals((prev) => ({
      ...prev,
      [currentKey]: {
        ...journal,
        moods: newMoods,
      },
    }));
  };
  const setSelectedSymptoms = (newSymptoms: string[]) => {
    setJournals((prev) => ({
      ...prev,
      [currentKey]: {
        ...journal,
        symptoms: newSymptoms,
      },
    }));
  };

  const toggleSelection = (item: string, list: string[], setList: (list: string[]) => void) => {
    if (list.includes(item)) {
      setList(list.filter((i) => i !== item));
    } else {
      setList([...list, item]);
    }
  };

  const handleVitalChange = (field: keyof JournalData['vitals'], value: string | [string, string]) => {
    setJournals((prev) => ({
      ...prev,
      [currentKey]: {
        ...journal,
        vitals: {
          ...journal.vitals,
          [field]: value,
        },
      },
    }));
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={COLORS.background} />
      {/* --- HEADER SECTION --- */}
      <View style={styles.headerContainer}>
        {/* Toggle Switch */}
        <View style={styles.toggleContainer}>
          <TouchableOpacity
            style={[styles.toggleBtn, activeTab === 'Journal' && styles.toggleBtnActive]}
            onPress={() => setActiveTab('Journal')}
          >
            <Text style={[styles.toggleText, activeTab === 'Journal' && styles.toggleTextActive]}>Journal</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.toggleBtn, activeTab === 'Kicks' && styles.toggleBtnActive]}
            onPress={() => setActiveTab('Kicks')}
          >
            <Text style={[styles.toggleText, activeTab === 'Kicks' && styles.toggleTextActive]}>Kicks Counter</Text>
          </TouchableOpacity>
        </View>
        {/* Date Navigator */}
        <View style={styles.dateRow}>
          <TouchableOpacity onPress={() => handleDateChange('prev')}>
            <Icon name="chevron-left" size={30} color={COLORS.text} />
          </TouchableOpacity>
          <Text style={styles.dateText}>{formatDate(currentDate)}</Text>
          <TouchableOpacity onPress={() => handleDateChange('next')}>
            <Icon name="chevron-right" size={30} color={COLORS.text} />
          </TouchableOpacity>
        </View>
      </View>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        {/* --- CARD 1: FEELING --- */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>How are you feeling?</Text>
          <TextInput
            style={styles.textArea}
            placeholder="Type here.."
            placeholderTextColor={COLORS.secondary}
            multiline
            value={journal.feeling}
            onChangeText={handleFeelingChange}
          />
        </View>
        {/* --- CARD 2: MOOD --- */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Mood</Text>
          <View style={styles.chipContainer}>
            {moods.map((mood) => (
              <Chip
                key={mood}
                label={mood}
                selected={journal.moods.includes(mood)}
                onPress={() => toggleSelection(mood, journal.moods, setSelectedMoods)}
              />
            ))}
          </View>
        </View>
        {/* --- CARD 3: SYMPTOMS --- */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Symptoms</Text>
          <View style={styles.chipContainer}>
            {symptoms.map((symptom) => (
              <Chip
                key={symptom}
                label={symptom}
                selected={journal.symptoms.includes(symptom)}
                onPress={() => toggleSelection(symptom, journal.symptoms, setSelectedSymptoms)}
              />
            ))}
          </View>
        </View>
        {/* --- CARD 4: VITALS --- */}
        <View style={styles.card}>
          <VitalRow
            label="Blood Pressure"
            unit=""
            isDoubleInput
            value={journal.vitals.bloodPressure}
            onChange={(v: [string, string]) => handleVitalChange('bloodPressure', v)}
          />
          <VitalRow
            label="Sugar Level"
            unit="mmol/L"
            value={journal.vitals.sugar}
            onChange={(v: string) => handleVitalChange('sugar', v)}
          />
          <VitalRow
            label="Heart Rate"
            unit="bpm"
            value={journal.vitals.heartRate}
            onChange={(v: string) => handleVitalChange('heartRate', v)}
          />
          <VitalRow
            label="Weight"
            unit="kg"
            value={journal.vitals.weight}
            onChange={(v: string) => handleVitalChange('weight', v)}
          />
        </View>
        {/* Spacer for bottom tab */}
        <View style={{ height: 80 }} />
      </ScrollView>
      {/* --- BOTTOM TAB BAR --- */}
      <View style={styles.bottomBar}>
        <TouchableOpacity style={styles.tabItem}>
          <Icon name="home" size={24} color={COLORS.primary} />
          <Text style={[styles.tabLabel, { color: COLORS.primary }]}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.tabItem}>
          <Icon name="book-open-variant" size={24} color="#999" />
          <Text style={styles.tabLabel}>Recipe</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.tabItem}>
          <Icon name="calendar-month" size={24} color="#999" />
          <Text style={styles.tabLabel}>Appointment</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.tabItem}>
          <Icon name="account" size={24} color="#999" />
          <Text style={styles.tabLabel}>Profile</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// --- STYLES ---
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  headerContainer: {
    alignItems: 'center',
    paddingVertical: 10,
    backgroundColor: COLORS.background,
  },
  // Toggle Switch Styles
  toggleContainer: {
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderWidth: 1,
    borderColor: COLORS.primary,
    borderRadius: 25,
    padding: 2,
    marginBottom: 15,
  },
  toggleBtn: {
    paddingVertical: 8,
    paddingHorizontal: 25,
    borderRadius: 20,
  },
  toggleBtnActive: {
    backgroundColor: COLORS.primary,
  },
  toggleText: {
    color: COLORS.text,
    fontWeight: '600',
    fontSize: 16,
  },
  toggleTextActive: {
    color: '#FFF',
  },
  // Date Row
  dateRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '90%',
  },
  dateText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  // ScrollView
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 10,
  },
  // Cards
  card: {
    backgroundColor: COLORS.card,
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    // Shadow for iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    // Elevation for Android
    elevation: 3,
    borderWidth: 1,
    borderColor: '#F0F0F0',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 10,
  },
  // Input Area
  textArea: {
    height: 100,
    textAlignVertical: 'top', // Android fix
    color: COLORS.text,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#EEEEEE',
    borderRadius: 10,
    padding: 10,
  },
  // Chips
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  chip: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 15,
    marginRight: 8,
    marginBottom: 8,
    borderWidth: 1,
  },
  chipUnselected: {
    backgroundColor: COLORS.secondary,
    borderColor: COLORS.secondary,
  },
  chipSelected: {
    backgroundColor: COLORS.secondary, // Keep background pinkish
    borderColor: COLORS.text, // Dark border to indicate selection like image
    borderWidth: 1.5,
  },
  chipText: {
    color: COLORS.text,
    fontWeight: '500',
  },
  // Vitals
  vitalRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  vitalLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.text,
    flex: 1,
  },
  vitalInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    justifyContent: 'flex-end',
  },
  vitalInput: {
    width: 60,
    height: 35,
    borderWidth: 1,
    borderColor: COLORS.text,
    borderRadius: 5,
    textAlign: 'center',
    color: COLORS.text,
    marginRight: 8,
  },
  vitalInputSmall: {
    width: 50,
    height: 35,
    borderWidth: 1,
    borderColor: COLORS.text,
    borderRadius: 5,
    textAlign: 'center',
    color: COLORS.text,
  },
  slashText: {
    fontSize: 20,
    color: COLORS.text,
    marginHorizontal: 5,
  },
  unitText: {
    color: COLORS.textLight,
    width: 50,
  },
  // Bottom Bar
  bottomBar: {
    flexDirection: 'row',
    backgroundColor: '#FFF',
    paddingVertical: 10,
    borderTopWidth: 1,
    borderTopColor: '#EEEEEE',
    justifyContent: 'space-around',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
  },
  tabItem: {
    alignItems: 'center',
  },
  tabLabel: {
    fontSize: 12,
    marginTop: 4,
    color: '#999',
  },
});