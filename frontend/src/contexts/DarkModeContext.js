import React, { createContext, useContext, useState, useEffect } from 'react';

const DarkModeContext = createContext();

export const useDarkMode = () => {
  const context = useContext(DarkModeContext);
  if (!context) {
    throw new Error('useDarkMode must be used within a DarkModeProvider');
  }
  return context;
};

export const DarkModeProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Check localStorage for saved preference
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });

  useEffect(() => {
    // ===================================================================
    // INSTANT THEME SWITCH - Works for BOTH dark-to-light AND light-to-dark
    // ===================================================================
    
    // STEP 1: Add .no-transitions class to FREEZE all transitions
    document.documentElement.classList.add('no-transitions');
    document.body.classList.add('no-transitions');
    
    // STEP 2: Force a reflow to ensure the freeze is applied
    void document.body.offsetHeight;
    
    // Save preference to localStorage
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
    
    // STEP 3: Apply/remove theme classes INSTANTLY (all transitions frozen)
    if (isDarkMode) {
      // Switch to DARK mode
      document.documentElement.classList.add('dark-mode');
      document.body.classList.add('dark-mode');
    } else {
      // Switch to LIGHT mode
      document.documentElement.classList.remove('dark-mode');
      document.body.classList.remove('dark-mode');
    }
    
    // STEP 4: Force another reflow to ensure theme is painted
    void document.body.offsetHeight;
    
    // STEP 5: Remove .no-transitions class to restore hover effects
    // Use requestAnimationFrame to ensure paint is complete
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        document.documentElement.classList.remove('no-transitions');
        document.body.classList.remove('no-transitions');
      });
    });
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(prev => !prev);
  };

  return (
    <DarkModeContext.Provider value={{ isDarkMode, toggleDarkMode }}>
      {children}
    </DarkModeContext.Provider>
  );
};
