import { useColorScheme } from 'nativewind';
import { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { View } from 'react-native';

import { themes } from '~/utils/colors';

export type ThemeType = 'light' | 'dark';

type ContextType = {
  theme: ThemeType;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ContextType>({ theme: 'light', toggleTheme: () => {} });

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const { colorScheme, setColorScheme } = useColorScheme();
  const [theme, setTheme] = useState<ThemeType>((colorScheme as ThemeType) || 'light');

  useEffect(() => {
    if (colorScheme) {
      setTheme(colorScheme as ThemeType);
    }
  }, [colorScheme]);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    setColorScheme(newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <View style={themes[colorScheme ?? 'light']} className="flex-1">
        {children}
      </View>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;
