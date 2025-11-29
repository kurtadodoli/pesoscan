import { useDarkMode } from '../contexts/DarkModeContext';

export const useDarkModeClasses = (baseClass = '') => {
  const { isDarkMode } = useDarkMode();
  
  const getClasses = (additionalClasses = '') => {
    const classes = [baseClass, additionalClasses].filter(Boolean).join(' ');
    return isDarkMode ? `${classes} dark-mode` : classes;
  };
  
  return {
    isDarkMode,
    getClasses,
    darkModeClass: isDarkMode ? 'dark-mode' : ''
  };
};
